/**
 * Caso #3
 * Mónica Alfaro Parrales - 2020132572 
 * Max Richard Lee Chung - 2019185076
*/

const sales = require("./Sale_Design.js");
const express = require('express');
const router = express.Router();
const date = require('date-and-time');

// localhost:3000/articulos
router.get("/articulos", async (request, response) => {
  try {
      const result = await sales.find().exec();
      response.send(result);
  } catch (error) {
      response.status(500).send(error);
  }
});

// localhost:3000/ownerCancel/-/-
router.get("/ownerCancel/:duennio/:articulo", async (request, response) => {
  try {
      // Busco el query para dar de baja
      const query = await sales.findOne({nombreDuennio: request.params.duennio, nombreArticulo: request.params.articulo});
      const change = query.set({activo: false});
      change.save();
      response.send("Se cambió a inactivo");
  } catch (error) {
      response.status(500).send(error);
  }
});

// localhost:3000/dateCancel
router.get("/dateCancel", async(request, response) => {
  try {
    // Obtengo la fecha actual
    const now = new Date();
    // Busco el query para dar de baja en donde el articulo se encuentre activo y la fecha maxima sea menor a la actual
    const query = await sales.updateMany({"$and" : [{"activo":true},{"fechaMaxima":{$lte : date.format(now, 'YYYY/MM/DD HH:mm:ss')}}]},{$set : {"activo":false}});
    response.send("Se cambiaron a inactivo");
  } catch (error) {
      response.status(500).send(error);
  }
});

// localhost:3000/daysLeft
router.get("/daysLeft", async(request, response) => {
  try {
    // Obtengo la fecha actual
    const now = new Date();
    // Busco el query para dar de baja en donde el articulo se encuentre activo y la fecha maxima sea mayor a la actual
    const query = await sales.find({"$and" : [{"activo":true},{"fechaMaxima":{$gte : date.format(now, 'YYYY/MM/DD HH:mm:ss')}}]});
    response.send(query);
  } catch (error) {
      response.status(500).send(error);
  }
});

// localhost:3000/newOffer/-/-/-/-
router.get("/newOffer/:duennio/:articulo/:subastador/:precio", async(request, response) => {
  try{
      // Preparo el formato a insertar del request
      const newPrice = {
          nombreArticulo: request.params.articulo, 
          nombreSubastador: request.params.subastador,
          precio: request.params.precio};
      // Busco el query a insertar la lista
      const query = await sales.findOneAndUpdate({
        nombreDuennio: request.params.duennio, 
        nombreArticulo: request.params.articulo},
        {$push:{preciosSubasta: newPrice}});
      response.send("Se ha hecho su oferta");
  } catch (error){
      response.status(500).send(error);
  }
});

// http://localhost:3000/sortBetweenPrices/-/-
router.get("/sortBetweenPrices/:min/:max", async(request, response) => {
  try{
    // Busca los articulos entre el precio inicial
    var query = await sales.where('precioInicial').gte(parseInt(request.params.min)).lte(parseInt(request.params.max));
    response.send(query)
   } catch (error){
    response.status(500).send(error);
   }
});

// http://localhost:3000/sortBetweenOld/-/-
router.get("/sortBetweenOld/:min/:max", async(request, response) => {
  try{
    // Busca los articulos entre un min y max de annios de antiguedad
    var query = await sales.where('annoAntiguedad').gte(parseInt(request.params.min)).lte(parseInt(request.params.max));
    response.send(query)
   } catch (error){
       response.status(500).send(error);
   }
});

// http://localhost:3000/add
router.post("/add/", async(request, response) => {
  try{
    // Crea la nueva instancia de articulo
    const query = new sales ({
      nombreDuennio: request.body.nombreDuennio,
      emailDuennio: request.body.emailDuennio,
      nombreArticulo: request.body.nombreArticulo,
      detalle: request.body.detalle,
      urlFoto: request.body.urlFoto,
      precioInicial: request.body.precioInicial,
      annoAntiguedad: request.body.annoAntiguedad,
      fechaMaxima: request.body.fechaMaxima,
      activo: request.body.activo
     })
     // Guarda la instancia en mongo
     query.save();
     response.send("Se guardó el nuevo artículo")
  } catch (error){
    response.status(500).send(error);
  }
});

// localhost:3000/active
router.get("/active", async(request, response) => {
  try{
    // Encuentra todos los articulos activos
     var query =  await sales.find({activo:"true"})
     response.send(query)
  } catch (error){
      response.status(500).send(error);
  }
});

module.exports = router;