function chart_artist_popularity(data) {

    // var data = [{"name":"Ariana Grande","popularity":33},{"name":"Robin","popularity":12},{"name":"Anne","popularity":41},{"name":"Mark","popularity":16},{"name":"Joe","popularity":59},{"name":"Eve","popularity":38},{"name":"Karen","popularity":21},{"name":"Kirsty","popularity":25},{"name":"Chris","popularity":30},{"name":"Lisa","popularity":47},{"name":"Tom","popularity":5},{"name":"Stacy","popularity":20},{"name":"Charles","popularity":13},{"name":"Mary","popularity":29}];

    // set the dimensions and margins of the graph
    var margin = {top: 20, right: 20, bottom: 30, left: 100},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    // set the ranges
    var y = d3.scaleBand()
            .range([height, 0])
            .padding(0.1);

    var x = d3.scaleLinear()
            .range([0, width]);
            
    // append the svg object to the body of the page
    // append a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        
    .append("g")
        .attr("transform", 
            "translate(" + margin.left + "," + margin.top + ")");

    // format the data
    data.forEach(function(d) {
        d.popularity = +d.popularity;
    });

    // Scale the range of the data in the domains
    x.domain([0, d3.max(data, function(d){ return d.popularity; })])
    y.domain(data.map(function(d) { return d.name; }));
    //y.domain([0, d3.max(data, function(d) { return d.popularity; })]);

    // append the rectangles for the bar chart
    svg.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        .attr("class", "bar")
        //.attr("x", function(d) { return x(d.popularity); })
        .attr("width", function(d) {return x(d.popularity); } )
        .attr("y", function(d) { return y(d.name); })
        .attr("height", y.bandwidth());

    // add the x Axis
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    // add the y Axis
    svg.append("g")
        .call(d3.axisLeft(y));

    return svg;
}
