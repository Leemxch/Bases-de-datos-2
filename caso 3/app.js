/**
 * Caso #3
 * Mónica Alfaro Parrales - 2020132572 
 * Max Richard Lee Chung - 2019185076
*/

const Express = require("express"); 
const Mongoose = require("mongoose");
const routes = require("./routes.js")
var app = Express();

Mongoose.connect("mongodb://localhost:27017/caso3", { useNewUrlParser: true })
    .then( () => {
        console.log('Connected to db')
    })
    .catch(error => console.log(`Not connected+${error.message}`));

//Port
app.set('port', process.env.PORT || 3000);

//Middleware
app.use(Express.json()); //Receive JSON data
app.use(Express.urlencoded({ extended: true })); 
//Returns middleware that only parses urlencoded bodies and only looks 
//at requests where the Content-Type header matches the type option

//Router
app.use(require('./routes.js'))

app.listen(app.get('port'), () => {
    console.log("Listening at port: "+app.get('port'));
    console.log("Funciona :D")
});

app.get('/', function(req, res){
    res.send('Bienvenido a la subasta');
});