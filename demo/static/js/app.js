// Initialize the Amazon Cognito credentials provider.
AWS.config.region = awsConfig.region;
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: awsConfig.identityPoolId,
});

var s3 = new AWS.S3({
  params: {Bucket: awsConfig.bucketName}
});

function uploadFile() {
  var files = document.getElementById('file_upload').files;
  if (!files.length) {
    return alert('Please choose a file to upload first.');
  }

  var folderName = document.getElementById('dir_name').value;
  if (folderName === '') {
	  folderName = 'demo';
  }

  var file = files[0];
  var fileName = file.name;
  var folderKey = encodeURIComponent(folderName) + '/';
  var fileKey = folderKey + fileName;
  s3.upload({
      Key: fileKey,
      Body: file,
    }, function(err, data) {
         if (err) {
           return alert('There was an error uploading your file: ', err.message);
         }
         alert('Successfully uploaded file.');
  });
}
