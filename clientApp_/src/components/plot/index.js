import React from "react";
import PropTypes from "prop-types";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";

// let options = {
//   //TODO: impprove this
//   chart: {
//     type: "scatter",
//     zoomType: "xy,"
//   },
//   plotOptions: {
//     grouping: false,
//     series: {
//       grouping: false
//     },
//     dataLabels: {
//       enabled: true
//     }
//   },
//   title: {
//     text: "Meaningful title"
//   }
// series: [
//   {
//     name: "named foo",
//     showInLegend: true,
//     color: " black",
//     formatter: function() {
//       console.log(this.id);
//       return this.id;
//     },
//     data: [
//       {
//         id: "one",
//         x: 15,
//         y: 50
//       },
//       { id: "two", x: 20, y: 30 }
//     ],
//     events: {
//       click: function(e) {
//         console.log(e.point.id);
//       }
//     }
//   },
//   {
//     title: "vins part",
//     color: "green",
//     data: [[135, 150]]
//   },
//   {
//     title: "example",
//     color: "red",
//     data: [1, 2, 3],
//     label: "labelone",
//     showInLegend: true
//   },
//   {
//     events: {
//       click: function() {
//         console.log(this);
//       }
//     },
//     title: "copy",
//     color: "blue",
//     label: "label2",
//     data: [
//       [161.2, 51.6],
//       [167.5, 59.0],
//       [159.5, 49.2],
//       [157.0, 63.0],
//       [155.8, 53.6],
//       [170.0, 59.0],
//       [159.1, 47.6],
//       [166.0, 69.8],
//       [176.2, 66.8],
//       [160.2, 75.2],
//       [172.5, 55.2],
//       [170.9, 54.2],
//       [172.9, 62.5],
//       [153.4, 42.0],
//       [160.0, 50.0],
//       [147.2, 49.8],
//       [168.2, 49.2],
//       [175.0, 73.2],
//       [157.0, 47.8],
//       [167.6, 68.8],
//       [159.5, 50.6],
//       [175.0, 82.5],
//       [166.8, 57.2],
//       [176.5, 87.8],
//       [170.2, 72.8],
//       [174.0, 54.5],
//       [173.0, 59.8],
//       [179.9, 67.3],
//       [170.5, 67.8],
//       [160.0, 47.0]
//     ]
//   },
//   {
//     title: "named Points",
//     showInLegend: true,
//     color: "yellow",
//     events: {
//       click: function() {
//         //alert(this);
//         console.log(this._i);
//         console.log(this.symbolIndex);
//         //console.log(this.index);
//         //console.log(this.points[this.index].foo);

//         //console.log(this.data);
//       }
//     },
//     data: [
//       { foo: "p1", x: 50, y: 70 },
//       { foo: "p4", x: 55, y: 75 },
//       { foo: "pdrölf", x: 60, y: 80 },
//       { foo: "p17", x: 65, y: 71 }
//     ]
//   }
// ]
//};

class Plot extends React.Component {
  constructor() {
    super();
    this.state = {
      isLoaded: false,
      data: null,
      options: {
        //TODO: impprove this
        chart: {
          type: "scatter",
          zoomType: "xy,"
        },
        plotOptions: {
          grouping: false,
          series: {
            grouping: false
          },
          dataLabels: {
            enabled: true
          }
        },
        title: {
          text: "Meaningful title"
        },
        series: []
      }
    };
  }

  // componentDidMount = () => {
  //   console.log(
  //     "after the fetch, this is the new data set beeing set",
  //     this.state.isLoaded
  //   );
  //   console.log("is Data loaded correclty?");
  //   options = {
  //     ...options,
  //     series: [...this.state.data]
  //   };
  // };

  shouldComponentUpdate = nextProps => {
    if (this.props.newCoordObject !== nextProps.newCoordObject) {
      console.log(
        // "triggers component update",
        // this.props.newCoordObject,
        nextProps.newCoordObject
      );
      let tempSeries = Object.assign(this.state.options.series, []);
      let tempSeriesObject = {
        data: [...this.state.options.series],
        title: nextProps.text
      };
      let dataObj = {
        color: "green",
        y: nextProps.newCoordObject.coordinate.y,
        x: nextProps.newCoordObject.coordinate.x,
        title: nextProps.newCoordObject.coordinate.title
      };
      //console.log(":::::", tempSeries);

      tempSeriesObject.data.push(dataObj);
      tempSeries.push(tempSeriesObject);
      this.setState({
        ...this.state,
        options: {
          ...this.state.object,
          series: tempSeries
        }
      });
      console.log(this.state.options.series);

      return true;
    }

    return true;
  };

  rerenderChartOnNewCoordObj = () => {
    if (Object.keys(this.props.newCoordObject).length > 0) {
      console.log("triggers rerenderChartOnNewCoordObj");
    }
  };

  componentWillMount = async () => {
    console.log("triggers the fetch the get all", this.state);
    //TODO: replace this
    if (!this.state.isLoaded) {
      //const url = "http://10.180.16.225:5000";
      const url = "http://api.textminer.quving.com/";
      const response = await fetch(url);
      const data = await response.json();

      if (!data) return;
      this.setState({
        isLoaded: true,
        //data
        options: {
          ...this.state.options,
          title: {
            text: data.name
          },
          series: data.series
        }
      });

      // this.state.options.series.forEach((series, index) => {
      //   this.setState({
      //     ...this.state,
      //     options: {
      //       ...this.state.options,
      //       series: {
      //         [index]: {
      //           events: {
      //             click: function(e) {
      //               console.log(e.point.id);
      //             }
      //           }
      //         }
      //       }
      //     }
      //   });
      // });
    }
  };

  render() {
    //console.log("render", this.state.options);
    // if (!this.state.isLoaded && this.state.options === null) {
    //   return <div>isloading....</div>;
    // }

    return (
      <>
        <HighchartsReact
          highcharts={Highcharts}
          options={this.state.options}
          onClick={this.onChartClick}
        />
      </>
    );
  }
}

Plot.propTypes = {
  newCoordObject: PropTypes.object
};

export default Plot;
