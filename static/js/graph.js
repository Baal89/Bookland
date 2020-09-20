var chart = new dc.BarChart('#book-rating');

d3.json('/data').then(function(jsonProject) {
    var ndx = crossfilter(jsonProject)
        bookDimension = ndx.dimension(function(d) {return d.book_title})
        sumGroup = bookDimension.group().reduce(
            function (p,v) {
                ++p.count;
                p.total += v.review_rating;
                if (p.count == 0) {
                    p.average = 0;
                } else {
                    p.average = p.total / p.count;
                }
                return p;
            },
            function (p, v) {
                --p.count;
                p.total -= v.review_rating;
                if (p.count == 0) {
                    p.average = 0;
                } else {
                    p.average = p.total / p.count;
                }
                return p;
            },
            function () {
                return {
                    count: 0,
                    total: 0,
                    average: 0
                };
            }
        );

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
        .valueAccessor(function (d) {
        	return d.value.average;
        })
        .outerPadding(0.05)
        .group(sumGroup);

    chart.render();
});

