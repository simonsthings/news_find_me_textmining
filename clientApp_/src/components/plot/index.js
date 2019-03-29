import React from "react";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";

const options = {
  //TODO: impprove this
  chart: {
    type: "scatter",
    zoomType: "xy,"
  },
  title: {
    text: "My chart"
  },
  series: [
    { title: "example", color: "red", data: [1, 2, 3] },
    {
      title: "copy",
      color: "blue",
      data: [
        [161.2, 51.6],
        [167.5, 59.0],
        [159.5, 49.2],
        [157.0, 63.0],
        [155.8, 53.6],
        [170.0, 59.0],
        [159.1, 47.6],
        [166.0, 69.8],
        [176.2, 66.8],
        [160.2, 75.2],
        [172.5, 55.2],
        [170.9, 54.2],
        [172.9, 62.5],
        [153.4, 42.0],
        [160.0, 50.0],
        [147.2, 49.8],
        [168.2, 49.2],
        [175.0, 73.2],
        [157.0, 47.8],
        [167.6, 68.8],
        [159.5, 50.6],
        [175.0, 82.5],
        [166.8, 57.2],
        [176.5, 87.8],
        [170.2, 72.8],
        [174.0, 54.5],
        [173.0, 59.8],
        [179.9, 67.3],
        [170.5, 67.8],
        [160.0, 47.0]
      ]
    }
  ]
};

class Plot extends React.Component {
  constructor() {
    super();
    this.state = {
      isLoaded: false,
      data: null
    };
  }

  componentWillMount = async () => {
    //TODO: replace this
    if (!this.state.isLoaded) {
      const url = "https://swapi.co/api/people/1";
      const response = await fetch(url);
      const data = await response.json();

      if (!data) return;

      this.setState({
        isLoaded: true,
        data
      });
    }
  };

  render() {
    if (!this.state.isLoaded && this.state.data === null) {
      return <div>isloading....</div>;
    }

    return (
      <>
        <HighchartsReact highcharts={Highcharts} options={options} />
      </>
    );
  }
}

export default Plot;
