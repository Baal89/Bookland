var chart = new dc.BarChart('#book-rating');

d3.json('/data').then(function(jsonProject) {
    var ndx = crossfilter(jsonProject)
        bookDimension = ndx.dimension(function(d) {return d.book_title})
        sumGroup = bookDimension.group().reduceSum(function(d) {return d.review_rating})

    chart
        .width(768)
        .height(380)
        .x(d3.scaleBand())
        .xUnits(dc.units.ordinal)
        .brushOn(false)
        .xAxisLabel('Book Title')
        .yAxisLabel('Rating')
        .dimension(bookDimension)
        .barPadding(0.1)
        .outerPadding(0.05)
        .group(sumGroup);

    chart.render();
});

