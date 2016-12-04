var dataset = [];

var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var path = d3.geoPath();

var x = d3.scaleLinear()
    .domain([1, 10])
    .rangeRound([600, 860]);

var color = d3.scaleThreshold()
    .domain(d3.range(2, 10))
    .range(d3.schemeBlues[9]);

var g = svg.append("g")
    .attr("class", "key")
    .attr("transform", "translate(0,40)");

g.selectAll("rect")
  .data(color.range().map(function(d) {
      d = color.invertExtent(d);
      if (d[0] == null) d[0] = x.domain()[0];
      if (d[1] == null) d[1] = x.domain()[1];
      return d;
    }))
  .enter().append("rect")
    .attr("height", 8)
    .attr("x", function(d) { return x(d[0]); })
    .attr("width", function(d) { return x(d[1]) - x(d[0]); })
    .attr("fill", function(d) { return color(d[0]); });

g.append("text")
    .attr("class", "caption")
    .attr("x", x.range()[0])
    .attr("y", -6)
    .attr("fill", "#000")
    .attr("text-anchor", "start")
    .attr("font-weight", "bold")
    .text("Unemployment rate");

g.call(d3.axisBottom(x)
    .tickSize(13)
    .tickFormat(function(x, i) { return i ? x : x + "%"; })
    .tickValues(color.domain()))
  .select(".domain")
    .remove();

d3.queue()
    .defer(d3.json, "https://d3js.org/us-10m.v1.json")
    .await(drawMap);

// TODO figure out how to make query from js data, and then how to send it over... also do we differentiate between single and trend? or abstract it?
function querySingleYear() {

  var year = $('[name="year_select"]').val();
  var counties = $('[name="counties_select"]').val();
  var minIncome = $('[name="min_income_field"]').val();
  var maxIncome = $('[name="max_income_field"]').val();

  $.get('/data/singleyear',
    {year: year, counties: counties, minIncome: minIncome, maxIncome: maxIncome},
    function (data) {
      dataset = d3.csvParse(data);
      d3.queue()
        .defer(d3.json, "https://d3js.org/us-10m.v1.json")
        .await(drawMap);
    })
    .done(function() {

    });

}

function queryYearToYear() {

  var startYear = $('[name="start_year_select"]').val();
  var endYear = $('[name="end_year_select"]').val();
  var attr = $('[name="year_to_year_attr_select"]').val();

  $.get('/data/y2y',
    {startYear: startYear, endYear: endYear, attr: attr},
    function (data) {
      dataset = d3.csvParse(data);
      printRows(dataset);
      d3.queue()
        .defer(d3.json, "https://d3js.org/us-10m.v1.json")
        .await(drawMap);
    })
    .done(function() {
      
    });
}

function printRows(dataset) {
  // add headers/column names
  $("#tableView").append('<tr>');
  for (var property in dataset[0]) {
    if(dataset[0].hasOwnProperty(property)) {
      $("#tableView").append("<th>" + property + "</th>");
    }
  }
  $("#tableView").append('</tr>');

  dataset.slice(0, 50).forEach(function (d) {
    $("#tableView").append('<tr>');
    for (var property in d) {
      if(d.hasOwnProperty(property)) {
        $("#tableView").append("<td>" + d[property] + "</td>");
      }
    }
    $("#tableView").append('</tr>');
  });
  
}

// TODO bug where redraw hides county lines
// TODO alaska disappeared
function drawMap(error, us) {
  if (error) throw error;

  var minVal = 0;
  var maxVal = 0;

  var dataMap = d3.map();
  dataset.forEach(function (d) {
    dataMap.set(d.fips, d.difference);
    minVal = Math.min(minVal, d.difference);
    maxVal = Math.max(maxVal, d.difference);
  });

  // TODO fix so that crazy outliers don't mess up scale
  color = color.domain(d3.range(minVal, maxVal, (maxVal - minVal)/10 ));

  svg.append("g")
      .attr("class", "counties")
    .selectAll("path")
    .data(topojson.feature(us, us.objects.counties).features)
    .enter().append("path")
      .attr("fill", function(d) { return color(d.rate = dataMap.get(d.id)); })
      .attr("d", path)
    .append("title")
      .text(function(d) { return d.rate + "%"; });

  svg.append("path")
      .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
      .attr("class", "states")
      .attr("d", path);
}