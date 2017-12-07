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