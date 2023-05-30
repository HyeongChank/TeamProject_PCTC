package com.example.pctcback.service;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.io.InputStreamReader;

@Service
public class ScrapyService {
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
            System.out.println(output.toString());
        }catch (IOException e){
            e.printStackTrace();
        }

    }


}
