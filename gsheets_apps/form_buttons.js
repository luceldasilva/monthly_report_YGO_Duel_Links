var mes_kog = "registro"; // Cambiar este en plantilla
var NUM_COLUMNA_BUSQUEDA = 11;

var hojaActiva = SpreadsheetApp.getActiveSpreadsheet();
var formulario = hojaActiva.getSheetByName("formulario");
var registro = hojaActiva.getSheetByName(mes_kog);


var celdas = [[
  formulario.getRange("B11").getValue(),
  formulario.getRange("D11").getValue(),
  formulario.getRange("F11").getValue(),
  formulario.getRange("H11").getValue(),
  formulario.getRange("B6").getValue(),
  formulario.getRange("D6").getValue(),
  formulario.getRange("F6").getValue(),
  formulario.getRange("B9").getValue(),
  formulario.getRange("D9").getValue(),
  formulario.getRange("F9").getValue()
]];

var valor = formulario.getRange("B3").getValue();
var valores = hojaActiva.getSheetByName(mes_kog).getDataRange().getValues(); // Nombre de hoja donde se almacenan datos


function Limpiar() {
  var celdasALimpiar = ["B3", "B6", "B9", "B11", "D6", "D9", "D11", "F6", "F9", "F11", "H11"];
  for (var i=0; i<celdasALimpiar.length; i++){
    formulario.getRange(celdasALimpiar[i]).clearContent();
  }
}


function Guardar() {
  // Por si es el mismo usuario con el mismo deck y
  // no dice que es cuenta secundaria
  // Para agregar otro deck del mismo usuario borrar la casilla del id
  if (valor !== "") {
    SpreadsheetApp.getUi().alert('Este usuario ya existe');
    return;
  }

  // Buscar la primera fila vacía en la columna A
  var columna = registro.getRange("A:A").getValues();
  var primeraFilaVacia = columna.findIndex(function(row) {
    return row[0] === "";  // Encuentra la primera celda vacía
  });

  // Si no hay filas vacías, empieza en la fila 2
  if (primeraFilaVacia === -1) {
    primeraFilaVacia = columna.length + 1;
  } else {
    primeraFilaVacia += 1;
  }

  // Verificar si alguno de los valores está vacío
  if (celdas[0].some(value => value !== "")) {
    registro.getRange(primeraFilaVacia, 1, 1, celdas[0].length).setValues(celdas);
  } else {
    SpreadsheetApp.getUi().alert('Algunos valores están vacíos.');
    return;
  }

  var celdaNumeroAleatorio = registro.getRange(primeraFilaVacia, NUM_COLUMNA_BUSQUEDA + 3);
  if (celdaNumeroAleatorio.getValue() === "") {
    var numeroAleatorio = Math.floor(Math.random() * 900000) + 100000;
    celdaNumeroAleatorio.setValue(numeroAleatorio);
  }

  Limpiar();
}


function Buscar() { 
  if (valor === "") {
    SpreadsheetApp.getUi().alert('No puedo encontrar la id');
    return;
  }
  
  for (var i = 0; i < valores.length; i++) {
    var fila = valores[i];
    if (fila[NUM_COLUMNA_BUSQUEDA] == valor) {
      formulario.getRange("B11").setValue(fila[0]);
      formulario.getRange("D11").setValue(fila[1]);
      formulario.getRange("F11").setValue(fila[2]);
      formulario.getRange("H11").setValue(fila[3]);
      formulario.getRange("B6").setValue(fila[4]);
      formulario.getRange("D6").setValue(fila[5]);
      formulario.getRange("F6").setValue(fila[6]);
      formulario.getRange("B9").setValue(fila[7]);
      formulario.getRange("D9").setValue(fila[8]);
      formulario.getRange("F9").setValue(fila[9]);
    }
  }
}


function Actualizar() {
  if (valor === "") {
    SpreadsheetApp.getUi().alert('Este es usuario nuevo, no puedo actualizar');
    return;
  }
  
  for (var i = 0; i < valores.length; i++) {
    var fila = valores[i];
    if(fila[NUM_COLUMNA_BUSQUEDA] == valor) {
      var INT_R = i+1

      registro.getRange(INT_R, 1, 1, celdas[0].length).setValues(celdas);
      // Cambia este valor si deseas usar otra columna para la fecha
      registro.getRange(INT_R, NUM_COLUMNA_BUSQUEDA + 2).setValue(new Date());
      
      SpreadsheetApp.getUi().alert('Datos actualizados');

      Limpiar();
    }
  }
}


function Eliminar() {
  var interface = SpreadsheetApp.getUi();
  var respuesta = interface.alert('¿Está seguro de borrar?',interface.ButtonSet.YES_NO);
  
  // Proceso si el usuario responde
  if (respuesta == interface.Button.YES) {
    for (var i = 0; i< valores.length; i++) {
      var fila = valores[i];
      if (fila[NUM_COLUMNA_BUSQUEDA] == valor) {
        var INT_R = i+1
        
        registro.deleteRow(INT_R);
        Limpiar();
      }
    }
  }
}