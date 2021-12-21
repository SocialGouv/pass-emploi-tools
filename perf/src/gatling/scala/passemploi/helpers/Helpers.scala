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
  
  
  def getAccessToken(authUrl: String, webUrl: String) = {
    exec {
      http("afficher login")
        .get(s"${authUrl}/auth/realms/pass-emploi/protocol/openid-connect/auth?client_id=pass-emploi-web&scope=openid%20email%20profile&response_type=id_token%20token&redirect_uri=${webUrl}%2Fapi%2Fauth%2Fcallback%2Fkeycloak&kc_idp_hint=&state=P0jYMdqicLo1DKamaMuu6PERhMZJ-M1Yz1LdxweHJ2Q&nonce=5fac3f353192858927a1cbeaa2d62f9ee0jLYNPgW")
        .check(status.is(200))
        .check(css("#kc-form-login")
          .ofType[Node]
          .transform(variabe => {
            variabe.getAttribute("action")
          })
          .saveAs("loginUrl"))
    }
      .exec { session =>
        println("LOGIN URL")
        println(session("loginUrl").as[String])
        session
      }
      .exec {
        http("se logger")
          .post("${loginUrl}")
          .formParam("username", "1")
          .formParam("password", "1")
          .formParam("credentialId", "")
          .disableFollowRedirect
          .check(status.is(302))
          .check(headerRegex("location", "access_token=(.*)&token_type").ofType[String].saveAs("token"))
      }
      .exec { session =>
        println("TOKEN")
        println(session("token").as[String])
        session
      }
  }
}
