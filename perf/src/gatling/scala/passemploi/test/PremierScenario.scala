package passemploi.test

import io.gatling.core.Predef._
import io.gatling.core.structure.ScenarioBuilder
import io.gatling.http.Predef._
import io.gatling.http.protocol.HttpProtocolBuilder
import passemploi.helpers.Helpers

class PremierScenario extends Simulation {
  val authUrl: String = Helpers.getProperty("AUTH_URL", "http://localhost:8082")
  val apiUrl: String = Helpers.getProperty("API_URL", "http://localhost:5000")
  val webUrl: String = Helpers.getProperty("WEB_URL", "http://localhost:3000")
  val clientSecret: String = Helpers.getProperty("AUTH_CLIENT_SECRET", "b208225f-addd-4600-8ae5-de6e19234551")
  var token: String = ""

  val httpProtocol: HttpProtocolBuilder = http
    .acceptHeader("*/*")
    .acceptEncodingHeader("gzip, deflate")
    .acceptLanguageHeader("en-GB,en-US;q=0.9,en;q=0.8")
    .userAgentHeader("Gatling")

  val authentification: ScenarioBuilder = scenario("Se connecter")
    .exec(Helpers.getAccessToken(authUrl, webUrl, clientSecret))
    .exec { session =>
      token = session("token").as[String]
      session
    }

  val scn: ScenarioBuilder = scenario("Premier Scenario")
    .exec {
      http("récupérer les jeunes")
        .get(s"${apiUrl}/conseillers/41/jeunes")
        .header("Authorization", session => s"Bearer ${token}")
        .check(status.is(200))
    }

  val usersPerSec: Double = Helpers.getProperty("USERS_PER_SEC", "100").toDouble
  val durationInSeconds: Int = Helpers.getProperty("DURATION_IN_SECONDS", "60").toInt

  setUp(
    authentification.inject(atOnceUsers(1))
      .andThen(
        scn.inject(
          rampUsersPerSec(1).to(usersPerSec).during(durationInSeconds)
        )
      )
  ).protocols(httpProtocol)
}
