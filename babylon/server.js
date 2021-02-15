var express = require('express');
var app     = express();
var http    = require('http').Server(app);
var cors = require('cors')

app.use(cors())
app.use(express.static(__dirname + '/public'));

http.listen(8080, function() {
  console.log("Server is listening on port http://127.0.0.1:8080/");
});
