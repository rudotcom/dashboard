"use strict";
! function() {
	let e, t;
	t = (isDarkStyle ? (e = config.colors_dark.textMuted, config.colors_dark) : (e = config.colors.textMuted, config.colors)).headingColor;
	let s = {
			donut: {
				series1: "rgba(221,160,55,0.86)",
				series2: "rgb(137,100,38)",
				series3: "rgba(228,198,233,0.77)",
				series4: "rgb(125,110,129)",
				series5: "rgba(78,221,65,0.2)",
				series6: "rgba(241,212,116,0.2)"
			},
			line: {
				series1: config.colors.warning,
				series2: config.colors.primary,
				series3: "#7367f029"
			}
		}
	let a = document.querySelector("#shipmentStatisticsChart"),
		d = JSON.parse(a.getAttribute("data-series")),
		r = {
			series: d['series'],
			type: "column",
			chart: {
				height: 220,
				stacked: !1,
				parentHeightOffset: 0,
				toolbar: {
					show: !0
				},
				zoom: {
					enabled: !1
				}
			},
			legend: {
				show: !0,
				position: "top",
				markers: {
					width: 20,
					height: 8,
					offsetX: -3
				},
				height: 40,
				itemMargin: {
					horizontal: 10,
					vertical: 0
				},
				fontSize: "25px",
				fontFamily: "Arial",
				fontWeight: 400,
				labels: {
					colors: t,
					useSeriesColors: !1
				},
				offsetY: 10
			},
			grid: {
				strokeDashArray: 8
			},
			colors: d['colors'],
			fill: {
				opacity: [1, 1]
			},
			plotOptions: {
				bar: {
					columnWidth: "70%",
					startingShape: "rounded",
					endingShape: "rounded",
					borderRadius: 2
				}
			},
			dataLabels: {
				enabled: !1
			},
			xaxis: {
				tickAmount: 10,
				categories: d['categories'],
				labels: {
					style: {
						colors: e,
						fontSize: "13px",
						fontFamily: "Arial",
						fontWeight: 400
					}
				},
				axisBorder: {
					show: !1
				},
				axisTicks: {
					show: !0
				}
			},
			yaxis: {
				tickAmount: d['yaxis']['tickAmount'],
				min: d['yaxis']['min'],
				max: d['yaxis']['max'],
				labels: {
					style: {
						colors: e,
						fontSize: "13px",
						fontFamily: "Arial",
						fontWeight: 400
					},
					formatter: function(e) {
						return e + " тыс.м²"
					}
				}
			},
			responsive: [{
				breakpoint: 1400,
				options: {
					chart: {
						height: 220
					},
					xaxis: {
						labels: {
							style: {
								fontSize: "10px"
							}
						}
					},
					legend: {
						itemMargin: {
							vertical: 0,
							horizontal: 10
						},
						fontSize: "13px",
						offsetY: 12
					}
				}
			}, {
				breakpoint: 1399,
				options: {
					chart: {
						height: 415
					},
					plotOptions: {
						bar: {
							columnWidth: "50%"
						}
					}
				}
			}, {
				breakpoint: 982,
				options: {
					plotOptions: {
						bar: {
							columnWidth: "30%"
						}
					}
				}
			}, {
				breakpoint: 480,
				options: {
					chart: {
						height: 250
					},
					legend: {
						offsetY: 7
					}
				}
			}]
		};
	null !== a && new ApexCharts(a, r).render();
}()
