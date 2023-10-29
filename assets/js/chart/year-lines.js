"use strict";
! function() {
	let o, r, e, t, s, i;
	i = (isDarkStyle ? (o = config.colors_dark.cardColor, r = config.colors_dark.headingColor, e = config.colors_dark.bodyColor, t = config.colors_dark.textMuted, config.colors_dark) : (o = config.colors.cardColor, r = config.colors.headingColor, e = config.colors.bodyColor, t = config.colors.textMuted, config.colors)).borderColor;

	let data = JSON.parse(document.querySelector("#yearShipmentChart").getAttribute("data-series"));
	let a = (document.querySelector("#yearShipmentChart")),
		n = {
			series: data['series'],
			colors: data['colors'],
			chart: {
				height: 255,
				parentHeightOffset: 0,
				parentWidthOffset: 0,
				toolbar: {
					show: !0
				},
				zoom: {
					enabled: !1
				},
				type: "area"
			},
			legend: {
				show: !0,
				position: "top",
				markers: {
					width: 18,
					height: 3,
					offsetX: -3
				},
				height: 40,
				itemMargin: {
					horizontal: 10,
					vertical: 0
				},
				fontSize: "15px",
				fontFamily: "Arial",
				fontWeight: 400,
				labels: {
					colors: t,
					useSeriesColors: !1
				},
				offsetY: 10
			},
			dataLabels: {
				enabled: !1
			},
			stroke: {
				width: 2,
				curve: "smooth"
			},
			fill: {
				type: "gradient",
				gradient: {
					shade: s,
					shadeIntensity: .6,
					opacityFrom: .5,
					opacityTo: .25,
					stops: [0, 95, 100]
				}
			},
			grid: {
				borderColor: i,
				strokeDashArray: 3,
				padding: {
					top: -20,
					bottom: -8,
					left: -10,
					right: 8
				}
			},
			xaxis: {
				categories: data['categories'],
				axisBorder: {
					show: !1
				},
				axisTicks: {
					show: !1
				},
				labels: {
					show: !0,
					style: {
						fontSize: "13px",
						colors: t
					}
				}
			},
			yaxis: {
				labels: {
					show: !0,
					formatter: function(e) {
						return new Intl.NumberFormat().format(e);
					}
				},
				min: data['yaxis']['min'],
				max: data['yaxis']['max'],
				tickAmount: data['yaxis']['tickAmount']
			}
		};
	null !== a && new ApexCharts(a, n).render();
	data = JSON.parse(document.querySelector("#yearSalesChart").getAttribute("data-series"));
	a = (document.querySelector("#yearSalesChart")),
		n = {
			series: data['series'],
			colors: data['colors'],
			chart: {
				height: 255,
				parentHeightOffset: 0,
				parentWidthOffset: 0,
				toolbar: {
					show: !0
				},
				zoom: {
					enabled: !1
				},
				type: "area"
			},
			legend: {
				show: !0,
				position: "top",
				markers: {
					width: 18,
					height: 3,
					offsetX: -3
				},
				height: 40,
				itemMargin: {
					horizontal: 10,
					vertical: 0
				},
				fontSize: "15px",
				fontFamily: "Arial",
				fontWeight: 400,
				labels: {
					colors: t,
					useSeriesColors: !1
				},
				offsetY: 10
			},
			dataLabels: {
				enabled: !1
			},
			stroke: {
				width: 2,
				curve: "smooth"
			},
			fill: {
				type: "gradient",
				gradient: {
					shade: s,
					shadeIntensity: .6,
					opacityFrom: .5,
					opacityTo: .25,
					stops: [0, 95, 100]
				}
			},
			grid: {
				borderColor: i,
				strokeDashArray: 3,
				padding: {
					top: -20,
					bottom: -8,
					left: -10,
					right: 8
				}
			},
			xaxis: {
				categories: data['categories'],
				axisBorder: {
					show: !1
				},
				axisTicks: {
					show: !1
				},
				labels: {
					show: !0,
					style: {
						fontSize: "13px",
						colors: t
					}
				}
			},
			yaxis: {
				labels: {
					show: !0,
					formatter: function(e) {
						return new Intl.NumberFormat().format(e);
					}
				},
				min: data['yaxis']['min'],
				max: data['yaxis']['max'],
				tickAmount: data['yaxis']['tickAmount']
			}
		};
	null !== a && new ApexCharts(a, n).render();
}()