// https://w3c.github.io/FileAPI/#FileReader-interface

var CUSTDATA_ID = 'custdata';
var CUSTDATA_UPLOAD_URL = '/custdataupload';
var CUSTDATA_FILE_INPUT_SEL = '#custdatafile';
var CUSTDATA_SUBMIT_INPUT_SEL = '#custdatasubmit';
var CUSTDATA_UPLOAD_STATUS_SEL = '#custdatastatus';
var CUSTDATA_PROGRESS_SEL = '#custdataprogress';
var CUSTDATA_PROGRESSDIV_SEL = '#custdataprogressdiv';


function updateStatus(msg, divstyle) {
    var div = document.createElement("div");
    div.className = divstyle || "statusmsg";
    div.append(msg);
    $(CUSTDATA_UPLOAD_STATUS_SEL).append(div);
}


// TODO: not implemented
function updateProgress(evt) {
    console.log(evt);
    var progressdiv = $(CUSTDATA_PROGRESSDIV_SEL);
    console.log(progressdiv);
    progressdiv.css('display', 'block');

    if (evt.lengthComputable) {
        // evt.loaded and evt.total are ProgressEvent properties
        var loaded = (evt.loaded / evt.total);
        if (loaded < 1) {
            $(CUSTDATA_PROGRESS_SEL).style.width = Math.floor(loaded) + "%";
        }
        $(CUSTDATA_PROGRESS_SEL).style.width = "100%";
    }
}


function errorHandler(evt) {
    switch (evt.target.error.code) {
    case evt.target.error.NOT_FOUND_ERR:
	updateStatus('File Not Found!');
	break;
    case evt.target.error.NOT_READABLE_ERR:
	updateStatus('File is not readable');
	break;
    case evt.target.error.ABORT_ERR:
	updateStatus('Aborted');
	break;
    default:
	updateStatus('An error occurred reading this file.');
    };
}


function postFile(evt) {
    console.log(evt);
    var result = evt.target.result;
    console.log(result);
    var data = new FormData();
    var file = $(CUSTDATA_FILE_INPUT_SEL).get(0).files[0];
    data.append(CUSTDATA_ID, file);
    $.ajax( {
        url: CUSTDATA_UPLOAD_URL,
        type: 'POST',
        data: data,
        processData: false,
        contentType: false
    }).done(function(response) {
        console.log(response);
        if (response['success']) {
            updateStatus('Server Responded: ' + response['success'] + ' successful updates');
        }
        for (var i = 0; i < response['errors'].length; i++) {
            updateStatus(response['errors'][i], "errormsg");
        }
        for (var i = 0; i < response['warnings'].length; i++) {
            updateStatus(response['warnings'][i], "warningmsg");
        }
    });
}


function uploadFile(evt) {
    updateStatus('Submitted!');
    evt.preventDefault();
    var fileInput = $(CUSTDATA_FILE_INPUT_SEL);
    console.log(fileInput);
    var files = fileInput.get(0).files;
    console.log(files);
    if (files.length) {
        file = files[0];
        updateStatus('Reading ' + file.name);
        var reader = new FileReader();
        // Read file into memory as UTF-8
        reader.readAsText(file, "UTF-8");
        // TODO: reader.onprogress = updateProgress;
        reader.onerror = errorHandler;
        reader.onload = postFile;
    }
    else {
        updateStatus('No file data to upload');
    }
}


$(document).ready(function() {
    console.log(CUSTDATA_UPLOAD_URL);
    updateStatus('Document Ready');
    $(document).on('click', CUSTDATA_SUBMIT_INPUT_SEL, uploadFile);
});

