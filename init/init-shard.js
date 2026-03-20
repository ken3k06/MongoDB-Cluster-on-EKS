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
