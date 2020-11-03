d3.json("/api/data").then(data => {
  console.log(data)
  var array1 = new Array;
var sel = document.getElementById("selectName");
for(var i = 0; i < data.length; i++) {
  var opt = document.createElement('option');
    opt.innerHTML = data[i]["artist"];
    opt.value = data[i]['followers']+' '+data[i]['images']+' '+data[i]['popularity'];
    sel.appendChild(opt);
}

})

function myFunction() {
  var x = document.getElementById("selectName").value;
  console.log(x)
  // document.getElementById("demo").innerHTML = x;
  // draw_graph(x)
  var res = x.split(' ')
  var x1 = res[0]
  var x2 = res[1]
  var x3 = res[2]
  console.log(x1)
  console.log(x2)
  console.log(x3)
  var demo = "Followers : "+x1+"   "+"   Popularity : "+x3
  document.getElementById("demo").innerHTML = (demo);
  document.getElementById("image").innerHTML = '<img src='+x2+' alt="Cheetah!" />'
}

// function myFunction1() {
//   var x = document.getElementById("selectName").value;
//   var res = x.split(":")
//   var x1=res[2]
//   console.log(x1)
//   // document.getElementById("demo").innerHTML = x;
//   draw_graph(x1)
// }

// function draw_graph(information){
//   document.getElementById("demo").innerHTML = information
//   var res = information.split(' ')
//   var x1 = res[0]
//   var x2 = res[1]
//   var x3 = res[3]
//   console.log(x1)
//   var img = document.createElement("img");
//       img.src = x2;
//   var src = document.getElementById("x");
//       src.appendChild(img);
// }

//myLink = 'https://api.spotify.com/v1/artists/${id}/top-tracks'

//d3.json(myLink).then(top_tracks => {
//  console.log(top_tracks)
//})
  // https://api.spotify.com/v1/audio-features
  // with a list of track ids

  //loop through tracks and get values and categories for radar into an array
  // values = []
  // categories = []
  
  // data = [{
  //   type: 'scatterpolar',
  //   r: [39, 28, 8, 7, 28, 15, 39],
  //   theta: ['A','B','C', 'D', 'E', 'F', 'A'],
  //   fill: 'toself'
  // }]
  
  // layout = {
  //   polar: {
  //     radialaxis: {
  //       visible: true,
  //       range: [0, 50]
  //     }
  //   },
  //   showlegend: false
  // }
  
  // Plotly.newPlot("myDiv", data, layout)




