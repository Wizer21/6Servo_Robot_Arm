var express = require('express');
var app     = express();
var http    = require('http').Server(app);
var cors = require('cors')

const bodyParser = require('body-parser')
const port = 8080

app.use(cors())
app.use(express.static(__dirname + '/public'));
app.use(bodyParser.urlencoded({ extended: false }))


app.get('/position/:list_list', async (request, answer) => {
  list = request.params.list_list
  console.log("GET ! " + list)

  if (list != ""){
    answer.status(200);
    answer.send("SUCCES " + list)
  }
  else{    
    answer.send("FAIL " + list)
    answer.status(404);  
  }
});

http.listen(8080, function() {
  console.log("Server is listening on port http://127.0.0.1:8080/");
});

