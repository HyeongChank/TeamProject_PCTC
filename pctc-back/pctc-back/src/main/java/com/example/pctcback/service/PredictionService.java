package com.example.pctcback.service;

import com.example.pctcback.model.Prediction;
import com.example.pctcback.model.PredictionTruck;
import com.example.pctcback.persistence.PredictionRepository;
import com.example.pctcback.persistence.PredictionTruckRepository;
import com.nimbusds.jose.shaded.gson.Gson;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

@Service
@Slf4j
public class PredictionService {
    @Autowired
    PredictionRepository predictionRepository;
    @Autowired
    PredictionTruckRepository predictionTruckRepository;
//    @Scheduled(fixedRate = 6000000)
    public void FlaskResponse() throws ParseException {
        RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        String jsonBody = "{}";
        headers.setContentType(MediaType.APPLICATION_JSON);
        String url = "http://10.125.121.220:5001/api/cnn_time_predict";
        HttpEntity<String> entity = new HttpEntity<>(jsonBody, headers);
        String response = restTemplate.postForObject(url, entity, String.class);
        Gson gson = new Gson();
        Data data = gson.fromJson(response, Data.class);
        List<Prediction> predictions = new ArrayList<>();

        for (int i = 0; i < data.time.size(); i++) {

            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("EEE, dd MMM yyyy HH:mm:ss zzz", Locale.ENGLISH);
            Double actual = data.actual_group.get(i);
            if (actual.isNaN()) {
                actual = Double.NaN;
            }
            LocalDateTime date = LocalDateTime.parse(data.time.get(i), formatter);
            Prediction prediction = new Prediction().builder()
                    .predict_group(data.predict_group.get(i))
                    .actual(actual)
                    .time(date)
                    .build();
            System.out.println("LocalDateTime: " + date);


            predictions.add(prediction);
        }
        predictionRepository.deleteAll();
        predictionRepository.saveAll(predictions);
    }
//    @Scheduled(fixedRate = 20000000)
    public void FlaskResponse2() throws ParseException {
        RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        String jsonBody = "{}";
        headers.setContentType(MediaType.APPLICATION_JSON);
        String url2 = "http://10.125.121.220:5001/api/cnn_count_predict";
        HttpEntity<String> entity2 = new HttpEntity<>(jsonBody,headers);
        String response2 =restTemplate.postForObject(url2, entity2, String.class);
        Gson gson2 = new Gson();
        Data data2 = gson2.fromJson(response2, Data.class);
        List<PredictionTruck> predictions2 = new ArrayList<>();
        for(int i =0; i<data2.time.size(); i++) {
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("EEE, dd MMM yyyy HH:mm:ss zzz", Locale.ENGLISH);
            LocalDateTime date = LocalDateTime.parse(data2.time.get(i), formatter);
            PredictionTruck prediction2 = new PredictionTruck().builder()
                    .predict_group(data2.predict_group.get(i))
                    .actual(data2.actual_group.get(i))
                    .time(date)
                    .build();
            System.out.println("LocalDateTime: " + date);
            predictions2.add(prediction2);
        }
        predictionTruckRepository.deleteAll();
        predictionTruckRepository.saveAll(predictions2);

    }


}
class Data {
    List<Double> actual_group;
    List<Double> predict_group;
    List<String> time;
}
