function page_ready()
 {
    test3();
    test1();
 }


 function test1()
 {
    var data = {
  // A labels array that can contain any sort of values
  labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
  // Our series array that contains series objects or in this case series data arrays
  series: [
    [5, 2, 4, 2, 1]
  ]
};
var options = {
  width: 300,  height: 200,
  plugins: [
    Chartist.plugins.ctPointLabels({
      textAnchor: 'middle'
    })
  ]
};
new Chartist.Line('#pointlabel', data, options);
    }

 function test3() {
 // https://github.com/tmmdata/chartist-plugin-tooltip
 var chart = new Chartist.Line('#tooltip-chart', {
  labels: [1, 2, 3],
  series: [
    [
      {meta: 'description', value: 1 },
      {meta: 'description', value: 5},
      {meta: 'description', value: 3}
    ],
    [
      {meta: 'other description', value: 2},
      {meta: 'other description', value: 4},
      {meta: 'other description', value: 2}
    ]
  ]
}, {
  low: 0,
  high: 8,
  fullWidth: true,
  plugins: [
    Chartist.plugins.tooltip()
  ],
  width: 300, height: 200
});
 }

 function test2() {
     new Chartist.Line('#chart1', {
        labels: [1, 2, 3, 4],
        series: [[100, 120, 180, 200]]
      });

      // Initialize a Line chart in the container with the ID chart2
      new Chartist.Bar('#chart2', {
        labels: [1, 2, 3, 4],
        series: [[5, 2, 8, 3]]
      });
  }

