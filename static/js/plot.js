d3.json("/api/artists").then(artists => {
  console.log(artists)
  // build dropdown!

})

d3.json('https://api.spotify.com/v1/artists/${id}/top-tracks').then(tracks => {
  // https://api.spotify.com/v1/audio-features
  // with a list of track ids

  // loop through tracks and get values and categories for radar into an array
  values = []
  categories = []

  data = [{
    type: 'scatterpolar',
    r: values,
    theta: categories,
    fill: 'toself'
  }]
  
  layout = {
    polar: {
      radialaxis: {
        visible: true,
        range: [0, 50]
      }
    },
    showlegend: false
  }
  
  Plotly.newPlot("myDiv", data, layout)

})

