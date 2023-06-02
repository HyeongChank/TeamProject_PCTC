package com.example.pctcback.persistence;

import com.example.pctcback.model.Prediction;
import com.example.pctcback.model.PredictionTruck;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;


@Repository
public interface PredictionTruckRepository extends JpaRepository<PredictionTruck, Long> {
    @Query("SELECT e FROM PredictionTruck e WHERE e.time = (SELECT MAX(e.time) FROM PredictionTruck e WHERE e.time <= :currentTime AND e.time >= :tenMinutesBefore)")
    PredictionTruck findClosestToCurrentTime(@Param("currentTime") LocalDateTime currentTime, @Param("tenMinutesBefore") LocalDateTime tenMinutesBefore);

    List<PredictionTruck> findTop11ByTimeLessThanEqualOrderByTimeDesc(LocalDateTime time);
    List<PredictionTruck> findTop10ByTimeGreaterThanOrderByTimeAsc(LocalDateTime time);




}
