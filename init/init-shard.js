rs.initiate(
{
    _id : "cfgReplSet",
    configsvr: true, 
    members: 
    [
        { _id : 0, host: "cfg-a:27017" },
        { _id : 1, host: "cfg-b:27017" },
        { _id: 2, host: "cfg-c:27017"  }
    ]
}
)
rs.initiate({
  _id: "sh1ReplSet",
  members: [
    { _id: 0, host: "sh1-a:27017" },
    { _id: 1, host: "sh1-b:27017" },
    { _id: 2, host: "sh1-c:27017" }
  ]
})

rs.initiate({
  _id: "sh2ReplSet",
  members: [
    { _id: 0, host: "sh2-a:27017" },
    { _id: 1, host: "sh2-b:27017" },
    { _id: 2, host: "sh2-c:27017" }
  ]
})
// After initiate all replica set, we need to add shards using mongos
// docker exec -it mongos mongosh 
// then 
// sh.addShard("sh1ReplSet/sh1-a:27017,sh1-b:27017,sh1-c:27017")
// sh.addShard("sh2ReplSet/sh2-a:27017,sh2-b:27017,sh2-c:27017")
