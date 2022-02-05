package passemploi.helpers

import io.gatling.core.Predef.{Node, css}
import io.gatling.http.Predef.{headerRegex, http, status}
import io.gatling.core.Predef._
import io.gatling.http.Predef._

object Helpers {
  def getProperty(propertyName: String, defaultValue: String) = {
    Option(System.getenv(propertyName))
      .orElse(Option(System.getProperty(propertyName)))
      .getOrElse(defaultValue)
  }


  def getAccessToken(authUrl: String, webUrl: String, clientSecret: String) = {
    exec {
      http("afficher login")
        .get(s"${authUrl}/auth/realms/pass-emploi/protocol/openid-connect/auth?client_id=pass-emploi-web&scope=openid%20email%20profile&response_type=code&redirect_uri=${webUrl}%2Fapi%2Fauth%2Fcallback%2Fkeycloak&kc_idp_hint=&state=P0jYMdqicLo1DKamaMuu6PERhMZJ-M1Yz1LdxweHJ2Q&nonce=5fac3f353192858927a1cbeaa2d62f9ee0jLYNPgW&code_challenge=P84fMlnfhamyT-Lv79Q3JWJLCvbWZouxikr4Ot8C8C0&code_challenge_method=S256")
        .check(status.is(200))
        .check(css("#kc-form-login")
          .ofType[Node]
          .transform(variabe => {
            variabe.getAttribute("action")
          })
          .saveAs("loginUrl"))
    }
      .exec {
        http("se logger")
          .post("${loginUrl}")
          .formParam("username", "41")
          .formParam("password", "41")
          .formParam("credentialId", "")
          .disableFollowRedirect
          .check(status.is(302))
          .check(headerRegex("location", "code=(.*)").ofType[String].saveAs("code"))
      }
      .exec {
        http("échanger le code contre le token")
          .post(s"${authUrl}/auth/realms/pass-emploi/protocol/openid-connect/token")
          .body(StringBody(session => s"grant_type=authorization_code&client_id=pass-emploi-web&client_secret=${clientSecret}&code=${session("code").as[String]}&redirect_uri=${webUrl}%2Fapi%2Fauth%2Fcallback%2Fkeycloak&code_verifier=aFrF4xUrQQm_vfivg2pcl19uer2AorbIjCRpdLWQZqwYYSfZVh-7tbJTOUrWrNV6-q10Fqw4x08qnmywqpO2CXiYThthaq_FFfDMZUsfs557wyik9.7jEJ-k-3FYuEd4"))
          .header("Content-Type", "application/x-www-form-urlencoded")
          .check(status.is(200))
          .check(jsonPath("$.access_token").saveAs("token"))
      }
  }
}
