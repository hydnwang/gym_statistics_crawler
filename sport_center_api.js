$(document).ready(function(){
		
		$("#gym").hide();
		$("#swim").hide();
		$("#ice").hide();

		api();
		setInterval(api, 60000);
		
		function api(){

			$.ajax({
				url: "https://yhcsc.cyc.org.tw/api", // 永和運動中心
                // https://xysc.cyc.org.tw/api 信義運動中心
                // https://dasc.cyc.org.tw/api 大安運動中心
				type: "POST",
				dataType: "json",
				error: function(xhr){
					console.log(xhr);
				},
				success: function(response){
					if(response.length == undefined && !(response["gym"][0].indexOf("找不到資源")!= -1))
					{
						$(".header3").show();
					}
					if(response["gym"] && !(response["gym"][0].indexOf("找不到資源")!= -1))
					{
						$("#gym").show();
						$('#gym_on').html(response["gym"][0]);
						$('#gym_all').html(response["gym"][1]);
					}
					if(response["swim"] && !(response["gym"][0].indexOf("找不到資源")!= -1))
					{
						$("#swim").show();
						$('#swim_on').html(response["swim"][0]);
						$('#swim_all').html(response["swim"][1]);
					}
					if(response["ice"] && !(response["gym"][0].indexOf("找不到資源")!= -1))
					{
						$("#ice").show();
						$('#ice_on').html(response["ice"][0]);
						$('#ice_all').html(response["ice"][1]);
					}
				},
				timeout: 10000
			});
		}
	})