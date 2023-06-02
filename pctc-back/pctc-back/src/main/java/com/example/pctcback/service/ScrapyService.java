package com.example.pctcback.service;

import com.example.pctcback.model.Ship;
import com.example.pctcback.persistence.ShipRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.io.InputStreamReader;
import java.util.List;

@Service
public class ScrapyService {
    private final ShipRepository shipRepository;
    @Autowired
    public ScrapyService(ShipRepository shipRepository) {
        this.shipRepository = shipRepository;
    }


    @Scheduled(fixedRate = 600000)
    public void runScrapyScript(){
        System.out.println("Scrapy is Starting..."); // 추후에 뺴서 둘것.
        ProcessBuilder processBuilder = new ProcessBuilder("scrapy","runspider","C:/Users/SW/Desktop/TeamProject/Scrapsite.py");
        try{
            Process process = processBuilder.start();
            InputStreamReader reader = new InputStreamReader(process.getInputStream());
            StringBuilder output = new StringBuilder();
            int ch;
            while ((ch = reader.read()) != -1) {
                output.append((char) ch);

            }
            String jsonString = output.toString();
            ObjectMapper mapper = new ObjectMapper();
            int  Cnt = 0;
            List<Ship> shipList = mapper.readValue(jsonString,mapper.getTypeFactory().constructCollectionType(List.class,Ship.class));
            shipRepository.deleteAll();
            shipRepository.saveAll(shipList);
        }catch (IOException e){
            e.printStackTrace();
        }

    }
    public List<Ship> PortStatus(){
        return shipRepository.findAll();
    }


}
