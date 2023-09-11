var mainApp = angular.module("mainApp", []);

$(function () {
    const video = $("video")[0];

    var model;
    var cameraMode = "environment"; // or "user"

    const startVideoStreamPromise = navigator.mediaDevices
        .getUserMedia({
            audio: false,
            video: {
                facingMode: cameraMode
            }
        })
        .then(function (stream) {
            return new Promise(function (resolve) {
                video.srcObject = stream;
                video.onloadeddata = function () {
                    video.play();
                    resolve();
                };
            });
        });

    var publishable_key = "rf_JCesTGXYaQWG7990JuApCxbYEaY2";
    var toLoad = {
        model: "car_detect-ao4mr",
        version: 1
    };

    const loadModelPromise = new Promise(function (resolve, reject) {
        roboflow
            .auth({
                publishable_key: publishable_key
            })
            .load(toLoad)
            .then(function (m) {
                model = m;
                resolve();
            });
    });

    Promise.all([startVideoStreamPromise, loadModelPromise]).then(function () {
        $("body").removeClass("loading");
        resizeCanvas();
        detectFrame();
    });

    var canvas, ctx;
    const font = "16px sans-serif";

    function videoDimensions(video) {
        // Ratio of the video's intrisic dimensions
        var videoRatio = video.videoWidth / video.videoHeight;

        // The width and height of the video element
        var width = video.offsetWidth,
            height = video.offsetHeight;

        // The ratio of the element's width to its height
        var elementRatio = width / height;

        // If the video element is short and wide
        if (elementRatio > videoRatio) {
            width = height * videoRatio;
        } else {
            // It must be tall and thin, or exactly equal to the original ratio
            height = width / videoRatio;
        }

        return {
            width: width,
            height: height
        };
    }

    $(window).resize(function () {
        resizeCanvas();
    });

    const resizeCanvas = function () {
        $("canvas").remove();

        canvas = $("<canvas/>");

        ctx = canvas[0].getContext("2d");

        var dimensions = videoDimensions(video);

        console.log(
            video.videoWidth,
            video.videoHeight,
            video.offsetWidth,
            video.offsetHeight,
            dimensions
        );

        canvas[0].width = video.videoWidth;
        canvas[0].height = video.videoHeight;

        canvas.css({
            width: dimensions.width,
            height: dimensions.height,
            left: ($(window).width() - dimensions.width) / 2,
            top: ($(window).height() - dimensions.height) / 2
        });

        $("body").append(canvas);
    };

    const renderPredictions = function (predictions) {
        var dimensions = videoDimensions(video);

        var scale = 1;

        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

        predictions.forEach(function (prediction) {
            const x = prediction.bbox.x;
            const y = prediction.bbox.y;

            const width = prediction.bbox.width;
            const height = prediction.bbox.height;

            // Draw the bounding box.
            ctx.strokeStyle = prediction.color;
            ctx.lineWidth = 4;
            ctx.strokeRect(
                (x - width / 2) / scale,
                (y - height / 2) / scale,
                width / scale,
                height / scale
            );

            // Draw the label background.
            ctx.fillStyle = prediction.color;
            const textWidth = ctx.measureText(prediction.class).width;
            const textHeight = parseInt(font, 10); // base 10
            ctx.fillRect(
                (x - width / 2) / scale,
                (y - height / 2) / scale,
                textWidth + 8,
                textHeight + 4
            );
        });

        predictions.forEach(function (prediction) {
            const x = prediction.bbox.x;
            const y = prediction.bbox.y;

            const width = prediction.bbox.width;
            const height = prediction.bbox.height;

            // Draw the text last to ensure it's on top.
            ctx.font = font;
            ctx.textBaseline = "top";
            ctx.fillStyle = "#000000";
            ctx.fillText(
                prediction.class,
                (x - width / 2) / scale + 4,
                (y - height / 2) / scale + 1
            );
        });
    };

    var prevTime;
    var pastFrameTimes = [];
    const detectFrame = function () {
        if (!model) return requestAnimationFrame(detectFrame);

        model
            .detect(video)
            .then(function (predictions) {
                requestAnimationFrame(detectFrame);
                renderPredictions(predictions);

                if (prevTime) {
                    pastFrameTimes.push(Date.now() - prevTime);
                    if (pastFrameTimes.length > 30) pastFrameTimes.shift();

                    var total = 0;
                    _.each(pastFrameTimes, function (t) {
                        total += t / 1000;
                    });

                    var fps = pastFrameTimes.length / total;
                    $("#fps").text(Math.round(fps));
                }
                prevTime = Date.now();
            })
            .catch(function (e) {
                console.log("CAUGHT", e);
                requestAnimationFrame(detectFrame);
            });
    };
});

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