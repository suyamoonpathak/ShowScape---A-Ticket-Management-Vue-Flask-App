<template>
  <CanvasJSChart
    :options="options"
    :style="styleOptions"
    @chart-ref="chartInstance"
    class="graph"
  />
</template>
<script>
export default {
  props: {
    capacityArray: Array,  // Prop to receive capacity data
    revenueArray: Array,   // Prop to receive revenue data
    theatreName: String,   // Prop to receive theatre name
  },
  data() {
    return {
      chart: null,
      options: {
        animationEnabled: true,
        exportEnabled: true,
        title: {
          text: `Revenue by Number of Bookings for ${this.theatreName}`,
        },
        axisY: {
          maximum: this.calculateMaxCapacity()+20,
          title: "Number of Bookings",
          titleFontColor: "#001232",
          labelFontColor: "#001232",
          lineColor: "#001232",
          tickColor: "#001232",
          gridColor: "#d3d3d3",
        },
        axisY2: {
          maximum: this.calculateMaxRevenue()+200,
          title: "Revenue Generated",
          valueFormatString: "$#,##0.##",
          titleFontColor: "#ff5252",
          labelFontColor: "#ff5252",
          lineColor: "#ff5252",
          tickColor: "#ff5252",
        },
        toolTip: {
          shared: true,
        },
        data: this.generateChartData()
      },
      styleOptions: {
        width: "100%",
        height: "360px",
      },
    };
  },
  methods: {
    generateChartData() {
      const capacitySeries = {
        type: "column",
        name: `Bookings`,
        dataPoints: this.capacityArray,
      };

      const revenueSeries = {
        type: "line",
        axisYType: "secondary",
        name: `Revenue`,
        dataPoints: this.revenueArray,
      };

      return [capacitySeries, revenueSeries];
    },

    calculateMaxCapacity() {
      return Math.max(...this.capacityArray.map(dataPoint => dataPoint.y));
    },
    calculateMaxRevenue() {
      return Math.max(...this.revenueArray.map(dataPoint => dataPoint.y));
    },

    chartInstance(chart) {
      this.chart = chart;
    },
  },
};
</script>
<style>
.graph{
    margin-bottom: 5%;
}
</style>
