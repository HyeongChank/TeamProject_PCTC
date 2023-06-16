package com.example.pctcback.controller;

import com.example.pctcback.model.Prediction;
import com.example.pctcback.model.PredictionTruck;
import com.example.pctcback.persistence.PredictionRepository;
import com.example.pctcback.persistence.PredictionTruckRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.*;

@RestController
public class DataController {
    @Autowired
    PredictionRepository predictionRepository;
    @Autowired
    PredictionTruckRepository predictionTruckRepository;

    @GetMapping("/getpredict")
    public ResponseEntity<?> PredictTime() throws Exception {
        LocalDateTime currentTime = LocalDateTime.now();
        currentTime= currentTime.withYear(2023).withMonth(3).withDayOfMonth(23);
        System.out.println("Current date and time: " + currentTime);
        LocalDateTime currentMinusTen = currentTime.minusMinutes(10);
        Prediction prediction =predictionRepository.findClosestToCurrentTime(currentTime,currentMinusTen);
        List<Prediction> actual = predictionRepository.findTop11ByTimeLessThanEqualOrderByTimeDesc(prediction.getTime());
        List<Prediction> future = predictionRepository.findTop10ByTimeGreaterThanOrderByTimeAsc(prediction.getTime());
        System.out.println(actual.get(1).toString());
        // 과거와 미래를 나눠서 List 에 담아서 보내기 (예측값은 빼고)
        Map<LocalDateTime, Double> resultMap = new HashMap<>();
        for (Prediction p : actual) {
            resultMap.put(p.getTime(), p.getActual());
        }
        for (Prediction p : future) {
            resultMap.put(p.getTime(), p.getPredict_group());
        }
        List<List<Object>> resultList = new ArrayList<>();
        for (Map.Entry<LocalDateTime, Double> entry : resultMap.entrySet()) {
            List<Object> item = new ArrayList<>();
            item.add(entry.getKey());
            item.add(entry.getValue());
            resultList.add(item);
        }
        resultList.sort(Comparator.comparing(item -> (LocalDateTime) item.get(0)));


        // Return the result
        return ResponseEntity.ok().body(resultList);

    }
    @GetMapping("/gettruck")
    public ResponseEntity<?> PredictTurck() throws Exception {
        LocalDateTime currentTime2 = LocalDateTime.now();
        currentTime2= currentTime2.withYear(2023).withMonth(3).withDayOfMonth(23);
//        LocalDateTime currentTime = LocalDateTime.of(2023,03,23,12,33,41);
        System.out.println("Current date and time: " + currentTime2);
        LocalDateTime currentMinusTen2 = currentTime2.minusMinutes(10);
        PredictionTruck prediction2 =predictionTruckRepository.findClosestToCurrentTime(currentTime2,currentMinusTen2);
        List<PredictionTruck> actual2 = predictionTruckRepository.findTop11ByTimeLessThanEqualOrderByTimeDesc(prediction2.getTime());
        List<PredictionTruck> future2 = predictionTruckRepository.findTop10ByTimeGreaterThanOrderByTimeAsc(prediction2.getTime());
        System.out.println(actual2.get(1).toString());
        // 과거와 미래를 나눠서 List 에 담아서 보내기 (예측값은 빼고)
        Map<LocalDateTime, Double> resultMap = new HashMap<>();
        for (PredictionTruck p : actual2) {
            resultMap.put(p.getTime(), p.getActual());
        }
        for (PredictionTruck p : future2) {
            resultMap.put(p.getTime(), p.getPredict_group());
        }
        List<List<Object>> resulttruckList = new ArrayList<>();
        for (Map.Entry<LocalDateTime, Double> entry : resultMap.entrySet()) {
            List<Object> item = new ArrayList<>();
            item.add(entry.getKey());
            item.add(entry.getValue());
            resulttruckList.add(item);
        }
        resulttruckList.sort(Comparator.comparing(item -> (LocalDateTime) item.get(0)));


        // Return the result
        return ResponseEntity.ok().body(resulttruckList);

    }




}
