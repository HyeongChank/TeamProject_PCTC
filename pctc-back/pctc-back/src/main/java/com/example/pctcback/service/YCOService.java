package com.example.pctcback.service;

import com.example.pctcback.model.YardCraneOperation;
import com.example.pctcback.model.YardStatus;
import com.example.pctcback.persistence.YardOperationRepository;
import com.example.pctcback.persistence.YardStatusRepository;
import jakarta.transaction.Transactional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.text.DecimalFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
@Slf4j
public class YCOService {
    String csvFilePath1 = "D:/SDH/TeamProject/TeamProject_PCTC/pctc-back/pctc-back/data/YardCrane0323.csv";
    String csvFilePath2 = "D:/SDH/TeamProject/TeamProject_PCTC/pctc-back/pctc-back/data/YardStatus.csv";
    String csvFilePath3 = "D:/SDH/TeamProject/TeamProject_PCTC/pctc-back/pctc-back/data/ScheduledContainer.csv";


    @Autowired
    private YardOperationRepository yardRepository;
    @Autowired
    private YardStatusRepository yardStatusRepository;

    public Map<String, Integer> ConNumBlock(List<String> blocks){
        Map<String,Integer> result = new HashMap<>();
        for(String block : blocks){
           int conNumbers = yardStatusRepository.findConNumbersByBlock(block);
            result.put(block, conNumbers);
        }
        return result;
    }



@Transactional
    public void myMethod(String csvFilePath) {
        try (BufferedReader br = new BufferedReader(new FileReader(csvFilePath))) {
            String line;
            boolean firstLine = true;
            yardStatusRepository.deleteAll();
            while ((line = br.readLine()) != null) {
                if (firstLine) {
                    firstLine = false;
                    continue;
                }

                String[] values = line.split(",");
                YardStatus yardStatus = YardStatus.builder()
                        .conNumber(values[0])
                        .shipCode(values[1])
                        .Conyear(Integer.parseInt(values[2]))
                        .voyage(values[3])
                        .operatorCode(values[4])
                        .fullOrEmpty(values[5].charAt(0))
                        .containerSizeCode(values[6])
                        .containerTypeCode(values[7])
                        .weightInTons(Double.parseDouble(values[8]))
                        .destinationCode(values[9])
                        .block(values[10])
                        .bay_x(Integer.parseInt(values[11]))
                        .row_y(Integer.parseInt(values[12]))
                        .tier_z(Integer.parseInt(values[13]))
                        .isExport("M".equals(values[14]))
                        .build();
//                yardStatusRepository.save(yardStatus);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }



    public void CreateYCO() {

        try (BufferedReader br = new BufferedReader(new FileReader(csvFilePath1))) {
            String line;
            boolean firstLine = true;
            while ((line = br.readLine()) != null) {
                if (firstLine) {
                    firstLine = false;
                    continue;
                }

                String[] values = line.split(",");
                SimpleDateFormat dateFormat = new SimpleDateFormat("yyyyMMddHHmmss");
                Date opCreationTime = dateFormat.parse(values[17].trim());
                Date opCompletionTime = dateFormat.parse(values[18].trim());
                long opTimeInSeconds = Long.parseLong(values[19]);
                Double opTimeInMinutes = opTimeInSeconds / 60.0;
                DecimalFormat df = new DecimalFormat("#.##");
                String ss = df.format(opTimeInMinutes);

                YardCraneOperation YCO = YardCraneOperation.builder()
                        .conNumber(values[0])
                        .opCode(values[1])
                        .shipCode(values[2])
                        .conYear(parseInt(values[3]))
                        .voyage(values[4])
                        .block(values[5])
                        .bay_x(parseInt(values[6]))
                        .row_y(parseInt(values[7]))
                        .tier_z(parseInt(values[8]))
                        .block2(values[9])
                        .bay_x2(parseInt(values[10]))
                        .row_y2(parseInt(values[11]))
                        .tier_z2(parseInt(values[12]))
                        .yardTruckNumber(values[13])
                        .fullOrEmpty(values[14].charAt(0))
                        .containerSizeCode(values[15])
                        .equipmentNumber(values[16])
                        .opCreationTime(opCreationTime)
                        .opCompletionTime(opCompletionTime)
                        .opTime(Double.valueOf(ss))
                        .build();
                yardRepository.save(YCO);


//
//                ScheduledContainer sc = new ScheduledContainer();
//                sc.setConNumber(values[0]);
//                sc.setContainerSizeCode(values[1]);
//                sc.setContainerTypeCode(values[2]);
//                sc.setShipCode(values[3]);
//                sc.setYearCol(Integer.parseInt(values[4]));
//                sc.setVoyage(values[5]);
//                sc.setWeight(Double.parseDouble(values[6]));
//                sc.setDestinationPort(values[7]);
//                sc.setShippingPort(values[8]);
//                SimpleDateFormat dateFormat1 = new SimpleDateFormat("MM/dd/yyyy HH:mm:ss");
//                Date time = dateFormat1.parse(values[9] + " " + values[10]);
//                sc.setTime(time);

            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private Integer parseInt(String value){
        if(value.isEmpty()){
            return null;
        }else{
            return Integer.parseInt(value);
        }

    }

}
