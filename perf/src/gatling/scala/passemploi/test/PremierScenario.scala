package passemploi.test

import io.gatling.core.Predef._
import io.gatling.core.structure.ScenarioBuilder
import io.gatling.http.Predef._
import io.gatling.http.protocol.HttpProtocolBuilder
import passemploi.helpers.Helpers
import io.gatling.core.Predef.{Node, css}
import io.gatling.http.Predef.{headerRegex, http, status}

class PremierScenario extends Simulation {
  val authUrl: String = Helpers.getProperty("AUTH_URL", "http://localhost:8082")
  val apiUrl: String = Helpers.getProperty("API_URL", "http://localhost:5000")
  val webUrl: String = Helpers.getProperty("WEB_URL", "http://localhost:3000")
  val clientSecret: String = Helpers.getProperty("AUTH_CLIENT_SECRET", "b208225f-addd-4600-8ae5-de6e19234551")

  val httpProtocol: HttpProtocolBuilder = http
    .acceptHeader("*/*")
    .acceptEncodingHeader("gzip, deflate")
    .acceptLanguageHeader("en-GB,en-US;q=0.9,en;q=0.8")
    .userAgentHeader("Gatling")

  val scn: ScenarioBuilder = scenario("Se connecter")
    .exec(Helpers.getAccessToken(authUrl, webUrl, clientSecret))
    .exec {
      http("récupérer les jeunes")
        .get(s"${apiUrl}/conseillers/41/jeunes")
        .header("Authorization", session => s"Bearer ${ session("token").as[String] }")
        .check(status.is(200))
        .check(bodyString.saveAs("bobody"))
    }
    .exec { session =>
      println("bobody")
      println(session("bobody").as[String])
      session
    }

  var usersPerSec = Helpers.getProperty("USERS_PER_SEC", "1").toDouble
  var durationInSeconds = Helpers.getProperty("DURATION_IN_SECONDS", "2").toInt
  setUp(
    scn.inject(
      rampUsersPerSec(1).to(1).during(1)
    ).protocols(httpProtocol))
}
