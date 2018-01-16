// Initialize the Amazon Cognito credentials provider.
AWS.config.region = awsConfig.region;
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: awsConfig.identityPoolId,
});

var s3 = new AWS.S3({
  params: {Bucket: awsConfig.bucketName}
});

var upload_timer;
var upload_counter = 0;
var to_be_processed = 0;

function waitForCompletion() {
  if (upload_counter < to_be_processed) {
	  console.log('File uploads not yet done...');
	  upload_timer = setTimeout(waitForCompletion, 2000);
  } else  {
    if (upload_timer) {
      clearTimeout(upload_timer);
      upload_timer = 0;
	}
    console.log('Done with file upload!');
    document.getElementById('popDiv').style.display = 'none';
  }
}

function uploadFile() {
  var files = document.getElementById('file_upload').files;
  if (!files.length) {
    return alert('Please choose a file to upload first.');
  }

  var folderName = document.getElementById('dir_name').value;
  if (folderName === '') {
	  folderName = 'demo';
  }

  upload_counter = 0;
  to_be_processed = files.length;

  upload_timer = setTimeout(waitForCompletion, 2000);

  var file;
  for (var i = 0; i < files.length; i++) {
	file = files[i];
    var fileName = file.name;
    var folderKey = encodeURIComponent(folderName) + '/';
    var fileKey = folderKey + fileName;
    console.log('Requesting file: ' + fileName);
    s3.upload({
        Key: fileKey,
        Body: file,
      }, function(err, data) {
        upload_counter += 1;
        if (err) {
          console.log('There was an error uploading your file: ' + data.key, err.message);
        } else {
          console.log('Successfully uploaded file: ' + data.key);
        }
      });
  }
  document.getElementById('popDiv').style.display = 'block';
  console.log('Waiting for completion...');
}
