lazy val root = (project in file(".")).
  settings(
    name := "classificationtree",
    version := "0.1",
    scalaVersion := "2.12.8",
    javaOptions in run += "-Xmx8G",
    resolvers += "Oscar Snapshots" at "http://artifactory.info.ucl.ac.be/artifactory/libs-snapshot/",
    libraryDependencies += "oscar" %% "oscar-cp" % "4.0.0-SNAPSHOT" withSources(),
    libraryDependencies += "org.scalactic" %% "scalactic" % "3.0.4",
    libraryDependencies += "org.scalatest" %% "scalatest" % "3.0.8" % "test",
        libraryDependencies += "oscar" %% "oscar-cp-xcsp3" % "4.0.0-SNAPSHOT" withSources()
  ).enablePlugins(PackPlugin)
  .settings(PackPlugin.packSettings)