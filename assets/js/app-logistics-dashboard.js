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
	let a, d, r;
		a = document.querySelector("#shipmentStatisticsChart"),
		d = JSON.parse(a.getAttribute("data-series")),
		r = {
			series: [{
				name: d[0]['name'],
				type: "column",
				data: d[0]['data'],
			},
				{
				name: d[1]['name'],
				type: "column",
				data: d[1]['data']
			}, ],
			chart: {
				height: 220,
				stacked: !1,
				parentHeightOffset: 0,
				toolbar: {
					show: !1
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
			colors: [config.colors.secondary, s.line.series1],
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
				categories: ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сент", "Окт", "Ноя", "Дек"],
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
					show: !1
				}
			},
			yaxis: {
				tickAmount: 4,
				min: 0,
				max: d[2]['max'],
				labels: {
					style: {
						colors: e,
						fontSize: "13px",
						fontFamily: "Arial",
						fontWeight: 400
					},
					formatter: function(e) {
						return e + " тыс.м2"
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
		a = document.querySelector("#saleStatisticsChart"),
		d = JSON.parse(a.getAttribute("data-series")),
		r = {
			series: [{
				name: d[0]['name'],
				type: "column",
				data: d[0]['data']
			},
				{
				name: d[1]['name'],
				type: "column",
				data: d[1]['data']
			}, ],
			chart: {
				height: 220,
				stacked: !1,
				parentHeightOffset: 0,
				toolbar: {
					show: !1
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
			colors: [config.colors.dark, config.colors.info],
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
				categories: ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"],
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
					show: !1
				}
			},
			yaxis: {
				tickAmount: 4,
				min: 0,
				max: d[2]['max'],
				labels: {
					style: {
						colors: e,
						fontSize: "13px",
						fontFamily: "Arial",
						fontWeight: 400
					},
					formatter: function(e) {
						return e + " тыс.р"
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
		let data = JSON.parse(document.querySelector("#productChart").getAttribute("data-series"));
		let total = document.querySelector("#productChart").getAttribute("data-total");
		a = (document.querySelector("#productChart")),
		r = {
			chart: {
				height: 520,
				parentHeightOffset: 0,
				type: "donut"
			},
			labels: data[0]['labels'],
			series: data[0]['series'],
			colors: data[0]['colors'],
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
									return total
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
}(), $(function() {
	var e = $(".dt-route-vehicles");
	e.length && (e.DataTable({
		ajax: assetsPath + "json/logistics-dashboard.json",
		columns: [{
			data: "id"
		}, {
			data: "id"
		}, {
			data: "location"
		}, {
			data: "start_city"
		}, {
			data: "end_city"
		}, {
			data: "warnings"
		}, {
			data: "progress"
		}],
		columnDefs: [{
			className: "control",
			orderable: !1,
			searchable: !1,
			responsivePriority: 2,
			targets: 0,
			render: function(e, t, s, a) {
				return ""
			}
		}, {
			targets: 1,
			orderable: !1,
			searchable: !1,
			checkboxes: !0,
			checkboxes: {
				selectAllRender: '<input type="checkbox" class="form-check-input">'
			},
			responsivePriority: 3,
			render: function() {
				return '<input type="checkbox" class="dt-checkboxes form-check-input">'
			}
		}, {
			targets: 2,
			responsivePriority: 1,
			render: function(e, t, s, a) {
				return '<div class="d-flex justify-content-start align-items-center user-name"><div class="avatar-wrapper"><div class="avatar me-2"><span class="avatar-initial rounded-circle bg-label-secondary"><i class="bx bxs-truck"></i></span></div></div><div class="d-flex flex-column"><a class="text-body fw-medium" href="app-logistics-fleet.html">VOL-' + s.location + "</a></div></div>"
			}
		}, {
			targets: 3,
			render: function(e, t, s, a) {
				return '<div class="text-body">' + s.start_city + ", " + s.start_country + "</div >"
			}
		}, {
			targets: 4,
			render: function(e, t, s, a) {
				return '<div class="text-body">' + s.end_city + ", " + s.end_country + "</div >"
			}
		}, {
			targets: -2,
			render: function(e, t, s, a) {
				var s = s.warnings,
					r = {
						1: {
							title: "No Warnings",
							class: "bg-label-success"
						},
						2: {
							title: "Temperature Not Optimal",
							class: "bg-label-warning"
						},
						3: {
							title: "Ecu Not Responding",
							class: "bg-label-danger"
						},
						4: {
							title: "Oil Leakage",
							class: "bg-label-info"
						},
						5: {
							title: "fuel problems",
							class: "bg-label-primary"
						}
					};
				return void 0 === r[s] ? e : '<span class="badge rounded ' + r[s].class + '">' + r[s].title + "</span>"
			}
		}, {
			targets: -1,
			render: function(e, t, s, a) {
				s = s.progress;
				return '<div class="d-flex align-items-center"><div div class="progress w-100" style="height: 8px;"><div class="progress-bar" role="progressbar" style="width:' + s + '%;" aria-valuenow="' + s + '" aria-valuemin="0" aria-valuemax="100"></div></div><div class="text-body ms-3">' + s + "%</div></div>"
			}
		}],
		order: [2, "asc"],
		dom: '<"table-responsive"t><"row d-flex align-items-center"<"col-sm-12 col-md-6"i><"col-sm-12 col-md-6"p>>',
		displayLength: 5,
		responsive: {
			details: {
				display: $.fn.dataTable.Responsive.display.modal({
					header: function(e) {
						return "Details of " + e.data().location
					}
				}),
				type: "column",
				renderer: function(e, t, s) {
					s = $.map(s, function(e, t) {
						return "" !== e.title ? '<tr data-dt-row="' + e.rowIndex + '" data-dt-column="' + e.columnIndex + '"><td>' + e.title + ":</td> <td>" + e.data + "</td></tr>" : ""
					}).join("");
					return !!s && $('<table class="table"/><tbody />').append(s)
				}
			}
		}
	}), $(".dataTables_info").addClass("pt-0"))
});