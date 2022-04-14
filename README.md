# FMEA_QC_Brachytherapy-App
A cool tool to evalute FMEA risk specific to patient for HDR GYN Brachy 
FQMBrachy is a tool for FMEA quality managment risk analysis in brachytherapy workflow. Tool is se to do this analysis for GYN HDR brachy, however, the platform is
build to work with other treatment sites (Head and neck, breast, prostate,....) and vraitey of the HDR sources. To do this the data base have to include the risk 
value for those workflow. 
AAPM TG-100 (2016), is published and include a typical FMEA risk analysis for IMRT. From 2016 till now (2022) severl brachytherapy TG is published 
{i.e, TG-221 (Ocular, 2019), TG-253 (skin, 2020), TG-182 (eBT, 2021), TG-229 (eBT dosi, 2021), TG-222 (mesh, 2021)}. All them recommended that the 
Failure Mode & Effect Analysis (FMEA) risk based QM to be part of brachy workflow. Presently there is no any software/App to evaluate FMEA risks for 
brachytherapy. Then the goal here was to create a WebApp to assess the risk in HDR GYN brachy treatment workflowfor each pateint. All the treatmnet 
memebr including Radiation Oncology Dr, Medical Physicit, Radiotherapist, .... can login to the APP and change the value of Occurance "O", Detectability
"D", and Severity "D" and finally Risk Priority Number "RPN" for that sub task specific to pateint, and save it in the database.
I used SQLlite 3 to biuld my databse, but due to confidentiality of the data, you have to make your own database. FQMBrachy, is able to do risk analysis 
specific to patient, and remind the treatment team, which process/substeps include more risk; which later can give a guide to department how they update
their treatmnet protocol,....
