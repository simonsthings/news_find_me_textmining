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
    {
      data: [1, 2, 3]
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
