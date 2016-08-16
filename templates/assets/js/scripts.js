/**
 * Created by amirmohsen on 8/16/16.
 */


var Handler = function () {
    this.DB = {
        domain: "",
        A: [],
        SOA: {},
        NS: [],
        MX: [],
        TXT: [],
        SRV:[],
        CNAME:[]
    };
};

Handler.prototype.setDomain = function (name) {
  this.DB.domain = name
};

Handler.prototype.addItem = function (type, content, ttl, address) {

    if(type == "A" || type == "NS" || type == "MX" || type == "CNAME"){
          this.DB[type].push({
              address:address,
              ttl:ttl,
              content: content
          });
    } else if (type == "SOA"){
        this.DB.SOA = {
              content:content,
              ttl:ttl
          };
    } else {
        this.DB[type].push({
              content:content,
              ttl:ttl
          });
    }
    console.log(this.DB);
};

Handler.prototype.remove = function(type, content, ttl){
    if(type == "SOA")
    {
        console.log(this.DB.SOA = {});
    } else {
        console.log(this.DB[type].splice(_.findIndex(this.DB[type], {content:content,ttl:ttl}), 1));
    }
    console.log(this.DB);
};

Handler.prototype.load = function (json) {
  this.DB = json;
    console.log(this.DB);
};

Handler.prototype.getJson = function () {
    return JSON.stringify(this.DB)
};