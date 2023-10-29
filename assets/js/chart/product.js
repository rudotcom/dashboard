"use strict";
! function() {
	let e, t;
	t = (isDarkStyle ? (e = config.colors_dark.textMuted, config.colors_dark) : (e = config.colors.textMuted, config.colors)).headingColor;
	let data = JSON.parse(document.querySelector("#productChart").getAttribute("data-series"));
	let a = (document.querySelector("#productChart")),
		r = {
		chart: {
			height: 520,
			parentHeightOffset: 0,
			type: "donut"
		},
		labels: data['labels'],
		series: data['series'],
		colors: data['colors'],
		stroke: {
			width: 3
		},
		dataLabels: {
			enabled: !1,
			formatter: function(e, t) {
				return parseInt(e) + "%"
			}
		},
		legend: {
			show: !0,
			position: "bottom",
			offsetY: 10,
			markers: {
				width: 20,
				height: 8,
				offsetX: -3
			},
			itemMargin: {
				horizontal: 10,
				vertical: 5
			},
			fontSize: "13px",
			fontFamily: "Arial",
			fontWeight: 400,
			labels: {
				colors: t,
				useSeriesColors: !1
			}
		},
		tooltip: {
			theme: !1
		},
		grid: {
			padding: {
				top: 15
			}
		},
		plotOptions: {
			pie: {
				donut: {
					size: "45%",
					labels: {
						show: !0,
						value: {
							fontSize: "26px",
							fontFamily: "Arial",
							color: t,
							fontWeight: 500,
							offsetY: -30,
							formatter: function(e) {
								return parseInt(e) + "%"
							}
						},
						name: {
							offsetY: 20,
							fontFamily: "Arial",
						},
						total: {
							show: !0,
							fontSize: "0.7rem",
							label: "Общий объем",
							color: e,
							formatter: function(e) {
								return data['total']
							}
						}
					}
				}
			}
		},
		responsive: [{
			breakpoint: 420,
			options: {
				chart: {
					height: 360
				}
			}
		}]
	};
	null !== a && new ApexCharts(a, r).render()
}();
