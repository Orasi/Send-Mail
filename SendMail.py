from Helpers.Results import UploadRegressionResults


page_method = UploadRegressionResults
myfile = open(page_method.results_file_name, 'r')
results = myfile.read()
page_method.send_mail(page_method, results)
myfile.close()