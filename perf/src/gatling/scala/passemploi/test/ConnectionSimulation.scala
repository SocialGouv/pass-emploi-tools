package passemploi.test

import io.gatling.core.Predef._
import io.gatling.core.structure.ScenarioBuilder
import io.gatling.http.Predef._
import io.gatling.http.protocol.HttpProtocolBuilder
import passemploi.helpers.Helpers

class ConnectionSimulation extends Simulation {
  val authUrl: String = Helpers.getProperty("AUTH_URL", "http://localhost:8082")
  val apiUrl: String = Helpers.getProperty("API_URL", "http://localhost:5000")
  val webUrl: String = Helpers.getProperty("WEB_URL", "http://localhost:3000")

  val httpProtocol: HttpProtocolBuilder = http
    .acceptHeader("*/*")
    .acceptEncodingHeader("gzip, deflate")
    .acceptLanguageHeader("en-GB,en-US;q=0.9,en;q=0.8")
    .userAgentHeader("Gatling")

  val scn: ScenarioBuilder = scenario("Se connecter")
    .exec(Helpers.getAccessToken(authUrl, webUrl))
  
  var usersPerSec=Helpers.getProperty("USERS_PER_SEC", "1").toDouble
  var durationInSeconds=Helpers.getProperty("DURATION_IN_SECONDS", "2").toInt
  setUp(
    scn.inject(
      rampUsersPerSec(1).to(100).during(300)
    ).protocols(httpProtocol))
}
