import React from 'react'
import Chart from 'react-apexcharts'
import './TopWordBarChart.css'

class TopWordBarChart extends React.Component {
    constructor(props) {
      super(props);

      this.state = {
        series:  [],
        options: {
          chart: {
            type: 'bar',
            height: 500,
          },
          plotOptions: {
            bar: {
              horizontal: false,
            },
          },
          stroke: {
            width: 1,
            colors: ['#fff']
          },
          title: {
            text: 'Tweet Top Words/Tags'
          },
          noData: {
            text: 'Loading...'
          },
          xaxis: {
            categories: [],
          },
          yaxis: {
            title: {
              text: undefined
            },
          },
          fill: {
            opacity: 1
          },
          legend: {
            position: 'top',
            horizontalAlign: 'left',
            offsetX: 40
          }
        },
      
      
      };
    }
    componentDidMount(){
        const startDate = String(this.props.startDate).slice(4, 24).replaceAll(' ', '-')
        const endDate = String(this.props.endDate).slice(4, 24).replaceAll(' ', '-')
        const isWordOrTag = this.props.isWordOrTag ? 'tag' : 'word'
        fetch(`http://127.0.0.1:8000/api/tweet/top/${isWordOrTag}/10/${startDate}/${endDate}`)
    .then(res => res.json())
    .then(
      (result) => {
        console.log(result)
        this.setState({
          series: result.series,
          options: {
            ...this.state.options,
            xaxis: {
              ...this.state.options.xaxis, 
                categories: result.name
              }
            }
        })
      },
      (error) => {
        this.setState({
            isLoaded: true,
            error
          });
      })
    }

    render() {
      return (
        <div className="app">
        <div className="row">
          <div className="mixed-chart">
            <Chart
              options={this.state.options}
              series={this.state.series}
              type="bar"
              width="800"
            />
          </div>
        </div>
      </div>
      );
    }
  }
export default TopWordBarChart;