"use strict";
! function() {
	let o, e, r, t, a, s, i, n, l, d;
	d = isDarkStyle ? (o = config.colors_dark.cardColor, e = config.colors_dark.headingColor, r = config.colors_dark.textMuted, t = config.colors_dark.bodyColor, s = config.colors_dark.borderColor, a = "dark", i = "#4f51c0", n = "#595cd9", l = "#8789ff", "#c3c4ff") : (o = config.colors.white, e = config.colors.headingColor, r = config.colors.textMuted, t = config.colors.bodyColor, s = config.colors.borderColor, a = "", i = "#e1e2ff", n = "#c3c4ff", l = "#a5a7ff", "#696cff");
	var c = {
		donut: {
			series1: config.colors.success,
			series2: "rgba(113, 221, 55, 0.6)",
			series3: "rgba(113, 221, 55, 0.4)",
			series4: "rgba(113, 221, 55, 0.2)"
		}
	};
	var h = document.querySelectorAll(".chart-progress"),
		h = (h && h.forEach(function(o) {
			var e = config.colors[o.dataset.color],
				r = o.dataset.series,
				e = {
					chart: {
						height: 55,
						width: 45,
						type: "radialBar"
					},
					plotOptions: {
						radialBar: {
							hollow: {
								size: "25%"
							},
							dataLabels: {
								show: !1
							},
							track: {
								background: config.colors_label.secondary
							}
						}
					},
					colors: [e],
					grid: {
						padding: {
							top: -15,
							bottom: -15,
							left: -5,
							right: -15
						}
					},
					series: [r],
					labels: ["Progress"]
				};
			new ApexCharts(o, e).render()
		}), document.querySelector("#monthlySalesChart")),
		p = {
			chart: {
				height: 200,
				toolbar: {
					show: !1
				},
				zoom: {
					enabled: !1
				},
				type: "line",
				dropShadow: {
					enabled: !0,
					enabledOnSeries: [1, 2, 3, 4],
					top: 7,
					left: 4,
					blur: 3,
					color: config.colors.secondary,
					opacity: .2
				}
			},
			series: [{
				name: "Средняя",
				data: [20, 54, 20, 38, 22, 28, 16, 19, 15, 12, 8, 5]
			}, {
				name: "Подольск",
				data: [22, 31, 33, 41, 14, 25, 34, 70, 34, 45, 47, 40]
			}, {
				name: "Истра",
				data: [20, 32, 22, 65, 40, 46, 65, 55, 41, 55, 40, 35]
			}, {
				name: "Воронеж",
				data: [11, 11, 33, 40, 35, 46, 23, 50, 33, 45, 33, 44]
			}, {
				name: "Ульяновск",
				data: [36, 63, 35, 33, 35, 54, 24, 44, 37, 45, 44, 32]
			}],
			stroke: {
				curve: "smooth",
				dashArray: [8, 0, 0, 0, 0],
				width: [3, 2, 3, 2, 2]
			},
			legend: {
				show: !1
			},
			colors: [s, config.colors.primary, config.colors.warning, config.colors.success, config.colors.danger],
			grid: {
				show: !0,
				borderColor: s,
				padding: {
					top: -20,
					bottom: -10,
					left: 0
				}
			},
			markers: {
				size: 6,
				colors: "transparent",
				strokeColors: "transparent",
				strokeWidth: 5,
				hover: {
					size: 6
				},
				discrete: [{
					fillColor: config.colors.white,
					seriesIndex: 2,
					dataPointIndex: 3,
					strokeColor: config.colors.warning,
					size: 6
				}, {
					fillColor: config.colors.white,
					seriesIndex: 1,
					dataPointIndex: 7,
					strokeColor: config.colors.primary,
					size: 6
				}, {
					fillColor: config.colors.danger,
					seriesIndex: 3,
					dataPointIndex: 1,
					strokeColor: config.colors.success,
					size: 6
				}]
			},
			xaxis: {
				labels: {
					style: {
						colors: r,
						fontSize: "13px"
					}
				},
				axisTicks: {
					show: !0
				},
				categories: ["", "Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"],
				axisBorder: {
					show: !1
				}
			},
			yaxis: {
				show: !0
			}
		},
		h = (null !== h && new ApexCharts(h, p).render(), document.querySelector("#monthlyPriceChart")),
		p = {
			chart: {
				height: 200,
				toolbar: {
					show: !1
				},
				zoom: {
					enabled: !1
				},
				type: "line",
				dropShadow: {
					enabled: !0,
					enabledOnSeries: [1, 2, 3, 4],
					top: 7,
					left: 4,
					blur: 3,
					color: config.colors.secondary,
					opacity: .2
				}
			},
			series: [{
				name: "Средняя",
				data: [20, 54, 20, 38, 22, 28, 16, 19, 15, 12, 8, 5]
			}, {
				name: "Подольск",
				data: [36, 63, 35, 33, 35, 54, 24, 44, 37, 45, 44, 32]
			}, {
				name: "Истра",
				data: [11, 11, 33, 40, 35, 46, 23, 50, 33, 45, 33, 44]
			}, {
				name: "Воронеж",
				data: [22, 31, 33, 41, 14, 25, 34, 70, 34, 45, 47, 40]
			}, {
				name: "Ульяновск",
				data: [20, 32, 22, 65, 40, 46, 65, 55, 41, 55, 40, 35]
			}],
			stroke: {
				curve: "smooth",
				dashArray: [8, 0, 0, 0, 0],
				width: [3, 2, 3, 2, 2]
			},
			legend: {
				show: !1
			},
			colors: [s, config.colors.primary, config.colors.warning, config.colors.success, config.colors.danger],
			grid: {
				show: !0,
				borderColor: s,
				padding: {
					top: -20,
					bottom: -10,
					left: 0
				}
			},
			markers: {
				size: 6,
				colors: "transparent",
				strokeColors: "transparent",
				strokeWidth: 5,
				hover: {
					size: 6
				},
				discrete: [{
					fillColor: config.colors.white,
					seriesIndex: 2,
					dataPointIndex: 3,
					strokeColor: config.colors.warning,
					size: 6
				}, {
					fillColor: config.colors.white,
					seriesIndex: 1,
					dataPointIndex: 7,
					strokeColor: config.colors.primary,
					size: 6
				}, {
					fillColor: config.colors.danger,
					seriesIndex: 3,
					dataPointIndex: 1,
					strokeColor: config.colors.success,
					size: 6
				}]
			},
			xaxis: {
				labels: {
					style: {
						colors: r,
						fontSize: "13px"
					}
				},
				axisTicks: {
					show: !0
				},
				categories: ["", "Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"],
				axisBorder: {
					show: !1
				}
			},
			yaxis: {
				show: !0
			}
		},
		h = (null !== h && new ApexCharts(h, p).render(), document.querySelector("#sessionsChart")),
		p = {
			chart: {
				height: 90,
				type: "area",
				toolbar: {
					show: !1
				},
				sparkline: {
					enabled: !0
				}
			},
			markers: {
				size: 6,
				colors: "transparent",
				strokeColors: "transparent",
				strokeWidth: 4,
				discrete: [{
					fillColor: config.colors.white,
					seriesIndex: 0,
					dataPointIndex: 8,
					strokeColor: config.colors.warning,
					strokeWidth: 2,
					size: 6,
					radius: 8
				}],
				hover: {
					size: 7
				}
			},
			grid: {
				show: !1,
				padding: {
					right: 8
				}
			},
			colors: [config.colors.warning],
			fill: {
				type: "gradient",
				gradient: {
					shade: a,
					shadeIntensity: .8,
					opacityFrom: .8,
					opacityTo: .25,
					stops: [0, 95, 100]
				}
			},
			dataLabels: {
				enabled: !1
			},
			stroke: {
				width: 2,
				curve: "straight"
			},
			series: [{
				data: [280, 280, 240, 240, 200, 200, 260, 260, 310]
			}],
			xaxis: {
				show: !1,
				lines: {
					show: !1
				},
				labels: {
					show: !1
				},
				axisBorder: {
					show: !1
				}
			},
			yaxis: {
				show: !1
			}
		},
		h = (null !== h && new ApexCharts(h, p).render(), document.querySelector("#leadsReportChart")),
		p = {
			chart: {
				height: 157,
				width: 135,
				parentHeightOffset: 0,
				type: "donut"
			},
			labels: ["Electronic", "Sports", "Decor", "Fashion"],
			series: [45, 58, 30, 50],
			colors: [c.donut.series1, c.donut.series2, c.donut.series3, c.donut.series4],
			stroke: {
				width: 0
			},
			dataLabels: {
				enabled: !1,
				formatter: function(o, e) {
					return parseInt(o) + "%"
				}
			},
			legend: {
				show: !1
			},
			tooltip: {
				theme: !1
			},
			grid: {
				padding: {
					top: 5,
					bottom: 5
				}
			},
			plotOptions: {
				pie: {
					donut: {
						size: "75%",
						labels: {
							show: !0,
							value: {
								fontSize: "1.5rem",
								fontFamily: "Public Sans",
								color: e,
								fontWeight: 500,
								offsetY: -15,
								formatter: function(o) {
									return parseInt(o) + "%"
								}
							},
							name: {
								offsetY: 20,
								fontFamily: "Public Sans"
							},
							total: {
								show: !0,
								fontSize: ".7rem",
								label: "1 Week",
								color: t,
								formatter: function(o) {
									return "32%"
								}
							}
						}
					}
				}
			}
		},
		c = (null !== h && new ApexCharts(h, p).render(), document.querySelector("#reportBarChart")),
		h = {
			chart: {
				height: 120,
				type: "bar",
				toolbar: {
					show: !1
				}
			},
			plotOptions: {
				bar: {
					barHeight: "60%",
					columnWidth: "50%",
					startingShape: "rounded",
					endingShape: "rounded",
					borderRadius: 4,
					distributed: !0
				}
			},
			grid: {
				show: !1,
				padding: {
					top: -35,
					bottom: -10,
					left: -10,
					right: -10
				}
			},
			colors: [config.colors_label.primary, config.colors_label.primary, config.colors_label.primary, config.colors_label.primary, config.colors.primary, config.colors_label.primary, config.colors_label.primary],
			dataLabels: {
				enabled: !1
			},
			series: [{
				data: [40, 95, 60, 45, 90, 50, 75]
			}],
			legend: {
				show: !1
			},
			xaxis: {
				categories: ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"],
				axisBorder: {
					show: !1
				},
				axisTicks: {
					show: !1
				},
				labels: {
					style: {
						colors: r,
						fontSize: "13px"
					}
				}
			},
			yaxis: {
				labels: {
					show: !1
				}
			}
		},
		p = (null !== c && new ApexCharts(c, h).render(), document.querySelector("#salesAnalyticsChart")),
		c = {
			chart: {
				height: 350,
				type: "heatmap",
				parentHeightOffset: 0,
				offsetX: -10,
				toolbar: {
					show: !1
				}
			},
			series: [{
				name: "1k",
				data: [{
					x: "Jan",
					y: "250"
				}, {
					x: "Feb",
					y: "350"
				}, {
					x: "Mar",
					y: "220"
				}, {
					x: "Apr",
					y: "290"
				}, {
					x: "May",
					y: "650"
				}, {
					x: "Jun",
					y: "260"
				}, {
					x: "Jul",
					y: "274"
				}, {
					x: "Aug",
					y: "850"
				}]
			}, {
				name: "2k",
				data: [{
					x: "Jan",
					y: "750"
				}, {
					x: "Feb",
					y: "3350"
				}, {
					x: "Mar",
					y: "1220"
				}, {
					x: "Apr",
					y: "1290"
				}, {
					x: "May",
					y: "1650"
				}, {
					x: "Jun",
					y: "1260"
				}, {
					x: "Jul",
					y: "1274"
				}, {
					x: "Aug",
					y: "850"
				}]
			}, {
				name: "3k",
				data: [{
					x: "Jan",
					y: "375"
				}, {
					x: "Feb",
					y: "1350"
				}, {
					x: "Mar",
					y: "3220"
				}, {
					x: "Apr",
					y: "2290"
				}, {
					x: "May",
					y: "2650"
				}, {
					x: "Jun",
					y: "2260"
				}, {
					x: "Jul",
					y: "1274"
				}, {
					x: "Aug",
					y: "815"
				}]
			}, {
				name: "4k",
				data: [{
					x: "Jan",
					y: "575"
				}, {
					x: "Feb",
					y: "1350"
				}, {
					x: "Mar",
					y: "2220"
				}, {
					x: "Apr",
					y: "3290"
				}, {
					x: "May",
					y: "3650"
				}, {
					x: "Jun",
					y: "2260"
				}, {
					x: "Jul",
					y: "1274"
				}, {
					x: "Aug",
					y: "315"
				}]
			}, {
				name: "5k",
				data: [{
					x: "Jan",
					y: "875"
				}, {
					x: "Feb",
					y: "1350"
				}, {
					x: "Mar",
					y: "2220"
				}, {
					x: "Apr",
					y: "3290"
				}, {
					x: "May",
					y: "3650"
				}, {
					x: "Jun",
					y: "2260"
				}, {
					x: "Jul",
					y: "1274"
				}, {
					x: "Aug",
					y: "965"
				}]
			}, {
				name: "6k",
				data: [{
					x: "Jan",
					y: "575"
				}, {
					x: "Feb",
					y: "1350"
				}, {
					x: "Mar",
					y: "2220"
				}, {
					x: "Apr",
					y: "2290"
				}, {
					x: "May",
					y: "2650"
				}, {
					x: "Jun",
					y: "3260"
				}, {
					x: "Jul",
					y: "1274"
				}, {
					x: "Aug",
					y: "815"
				}]
			}, {
				name: "7k",
				data: [{
					x: "Jan",
					y: "575"
				}, {
					x: "Feb",
					y: "1350"
				}, {
					x: "Mar",
					y: "1220"
				}, {
					x: "Apr",
					y: "1290"
				}, {
					x: "May",
					y: "1650"
				}, {
					x: "Jun",
					y: "1260"
				}, {
					x: "Jul",
					y: "3274"
				}, {
					x: "Aug",
					y: "815"
				}]
			}, {
				name: "8k",
				data: [{
					x: "Jan",
					y: "575"
				}, {
					x: "Feb",
					y: "350"
				}, {
					x: "Mar",
					y: "220"
				}, {
					x: "Apr",
					y: "290"
				}, {
					x: "May",
					y: "650"
				}, {
					x: "Jun",
					y: "260"
				}, {
					x: "Jul",
					y: "274"
				}, {
					x: "Aug",
					y: "815"
				}]
			}],
			plotOptions: {
				heatmap: {
					enableShades: !1,
					radius: "6px",
					colorScale: {
						ranges: [{
							from: 0,
							to: 1e3,
							name: "1k",
							color: i
						}, {
							from: 1001,
							to: 2e3,
							name: "2k",
							color: n
						}, {
							from: 2001,
							to: 3e3,
							name: "3k",
							color: l
						}, {
							from: 3001,
							to: 4e3,
							name: "4k",
							color: d
						}]
					}
				}
			},
			dataLabels: {
				enabled: !1
			},
			stroke: {
				width: 4,
				colors: [o]
			},
			legend: {
				show: !1
			},
			grid: {
				show: !1,
				padding: {
					top: -10,
					left: 10,
					right: -15,
					bottom: 0
				}
			},
			xaxis: {
				labels: {
					show: !0,
					style: {
						colors: r,
						fontSize: "13px"
					}
				},
				axisBorder: {
					show: !1
				},
				axisTicks: {
					show: !1
				}
			},
			yaxis: {
				labels: {
					style: {
						colors: r,
						fontSize: "13px"
					}
				}
			},
			responsive: [{
				breakpoint: 1441,
				options: {
					chart: {
						height: "325px"
					},
					grid: {
						padding: {
							right: -15
						}
					}
				}
			}, {
				breakpoint: 1045,
				options: {
					chart: {
						height: "300px"
					},
					grid: {
						padding: {
							right: -50
						}
					}
				}
			}, {
				breakpoint: 992,
				options: {
					chart: {
						height: "320px"
					},
					grid: {
						padding: {
							right: -50
						}
					}
				}
			}, {
				breakpoint: 767,
				options: {
					chart: {
						height: "400px"
					},
					grid: {
						padding: {
							right: 0
						}
					}
				}
			}, {
				breakpoint: 568,
				options: {
					chart: {
						height: "330px"
					},
					grid: {
						padding: {
							right: -20
						}
					}
				}
			}],
			states: {
				hover: {
					filter: {
						type: "none"
					}
				},
				active: {
					filter: {
						type: "none"
					}
				}
			}
		},
		h = (null !== p && new ApexCharts(p, c).render(), document.querySelector("#salesStats")),
		p = {
			chart: {
				height: 340,
				type: "radialBar"
			},
			series: [75],
			labels: ["Sales"],
			plotOptions: {
				radialBar: {
					startAngle: 0,
					endAngle: 360,
					strokeWidth: "70",
					hollow: {
						margin: 50,
						size: "75%",
						image: assetsPath + "img/icons/misc/arrow-star.png",
						imageWidth: 65,
						imageHeight: 55,
						imageOffsetY: -35,
						imageClipped: !1
					},
					track: {
						strokeWidth: "50%",
						background: s
					},
					dataLabels: {
						show: !0,
						name: {
							offsetY: 60,
							show: !0,
							color: r,
							fontSize: "15px"
						},
						value: {
							formatter: function(o) {
								return parseInt(o) + "%"
							},
							offsetY: 20,
							color: e,
							fontSize: "32px",
							show: !0
						}
					}
				}
			},
			fill: {
				type: "solid",
				colors: config.colors.success
			},
			stroke: {
				lineCap: "round"
			},
			states: {
				hover: {
					filter: {
						type: "none"
					}
				},
				active: {
					filter: {
						type: "none"
					}
				}
			}
		};
	null !== h && new ApexCharts(h, p).render()
}();