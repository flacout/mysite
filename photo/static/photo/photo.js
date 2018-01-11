var image;
var imagegray;
var imagered=null;
var canvas;


function autoUpload() {
  var upload = document.getElementById("lastPicture");
  image = new SimpleImage(upload);
  imagegray = new SimpleImage(upload);
  imagered = new SimpleImage(upload);
  //Get canvas
  canvas = document.getElementById("can");
  image.drawTo(canvas);
}

function upload() {
  // "id_photo" is a field of the formated  {{form.as_table}}
  // It's in the final HTML file, it just appear dynamicaly.
  var upload = document.getElementById("id_photo");
  image = new SimpleImage(upload);
  imagegray = new SimpleImage(upload);
  imagered = new SimpleImage(upload);
  //Get canvas
  canvas = document.getElementById("can");
  image.drawTo(canvas);
}

function makeGray() {
  for (var pixel of imagegray.values()) {
    var avg = (pixel.getRed()+pixel.getGreen()+pixel.getBlue())/3;
    pixel.setRed(avg);
    pixel.setGreen(avg);
    pixel.setBlue(avg);
  }
  imagegray.drawTo(canvas);
}

function doDarker(){
  var slide=document.getElementById("slide");
  var slideValue=slide.value;
  var imagegray2= new SimpleImage(imagegray);
  for (var pixel of imagegray2.values()){
    x=pixel.getRed();
    pixel.setRed(x-slideValue);
    pixel.setGreen(x-slideValue);
    pixel.setBlue(x-slideValue);
  }
  imagegray2.drawTo(canvas);
}

function makeRed() {
  for (var pixel of imagered.values()) {
    var avg = (pixel.getRed()+pixel.getGreen()+pixel.getBlue())/3;
    if (avg<128){
      pixel.setRed(avg*2);
      pixel.setGreen(0);
      pixel.setBlue(0);
    }
    else{
      pixel.setRed(255);
      pixel.setGreen(avg*2-255);
      pixel.setBlue(avg*2-255);      
    }
  }
  imagered.drawTo(canvas);
}

function reset(){
  var context = canvas.getContext("2d");
  context.clearRect(0,0,canvas.width,canvas.height);
  upload();
  image.drawTo(canvas);
}

function saveModif() {
    var type = $("#photo_extension").val();
    if (type == 'jpeg' || type == 'jpg'){
      var dataURL = canvas.toDataURL('image/jpeg', 1.0);
    }
    else {
      var dataURL = canvas.toDataURL();
    }
    document.getElementById("textData").value = dataURL;
}

function isValidForm(){
    var type = $("#photo_id").val();
    if (type == '') { 
      alert("use SaveUpload first before modifying the picture");
      return false;
    }
}
