var mainApp = angular.module("mainApp", []);




mainApp.controller("mainAppController", function ($scope, $interval) {
  $scope.ns = "";

  // Agar scope dapat diakses sebagai global variabel
  window.$scope = $scope;

  // Simple Timer
  $interval(function () {
  }, 1000);


  //Global Variabel
  $scope.total_harga = ''
  $scope.total_liter = ''


  //Ini URL untuk Camera
  $scope.frame_field = "http://" + window.location.hostname + ":9901" + "/stream?topic=" + $scope.ns + "/frame_detect&type=ros_compressed";
  $scope.source = new EventSource("/send_detect_information");
  $scope.source.onmessage = function(event) {
    var data = event.data;
    // document.getElementById("data-container").innerHTML = data;
    var html_element_license_plate = document.getElementById("license-plate-span")
    var html_element_status_subsidi = document.getElementById("status-subsidi-span")
    var html_element_submit_button = document.getElementById("submit-request-button")


    var subscribed_data = data.split(';')
    html_element_license_plate.innerHTML = subscribed_data[0]

    if (subscribed_data[1] == '1') {
        
        html_element_status_subsidi.innerHTML = 'Subsidi Valid'
        html_element_status_subsidi.classList.remove("bg-red-500")
        html_element_status_subsidi.classList.add("bg-green-500")
        html_element_submit_button.disabled = false
      
    }
    else{
        html_element_status_subsidi.classList.remove("bg-green-500")
        html_element_status_subsidi.classList.add("bg-red-500")
        html_element_status_subsidi.innerHTML = 'Subsidi Tidak Valid'
        html_element_submit_button.disabled = true
        
    }

    };


  //Ini merupakan fungsi umum dalam html
  $scope.changeValue = function (value) {
    console.log('test')
    var html_element_liter_total = document.getElementById("liter-total-span")
    var html_element_harga_total = document.getElementById("harga-total-span")


    if (value == 12) {
        $scope.total_harga = $scope.total_harga.slice(0, -1);
        
    }
    else if (value == 11) {
        $scope.total_harga += `000`
        
    }
    else{
        $scope.total_harga += `${value}`
    }

    html_element_harga_total.innerHTML = `${Number($scope.total_harga)}`
    html_element_liter_total.innerHTML = `${Number($scope.total_harga) / 10000}`

    
  }


  $scope.send_request_data = function () {
    var html_element_liter_total = document.getElementById("liter-total-span")
    var html_element_license_plate = document.getElementById("license-plate-span")
    var html_element_status_subsidi = document.getElementById("status-subsidi-span")
    var req_string = `${html_element_liter_total.innerHTML};${html_element_license_plate.innerHTML};${html_element_status_subsidi.innerHTML}`
    console.log(req_string)


    fetch('/dashboard_request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            input_string: req_string
        })
    })
    .then(response => response.json())
    .then(data => {
        // Display the result
        console.log(data.result);
    })
    .catch(error => {
        console.error('Error:', error);
    });

  }

  




  
});