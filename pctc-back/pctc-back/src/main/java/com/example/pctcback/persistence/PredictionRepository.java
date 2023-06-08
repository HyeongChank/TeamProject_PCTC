package com.example.pctcback.persistence;

import com.example.pctcback.model.Prediction;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;


@Repository
public interface PredictionRepository extends JpaRepository<Prediction , Long> {
    @Query("SELECT e FROM Prediction e WHERE e.time = (SELECT MAX(e.time) FROM Prediction e WHERE e.time <= :currentTime AND e.time >= :tenMinutesBefore)")
    Prediction findClosestToCurrentTime(@Param("currentTime") LocalDateTime currentTime, @Param("tenMinutesBefore") LocalDateTime tenMinutesBefore);

    List<Prediction> findTop11ByTimeLessThanEqualOrderByTimeDesc(LocalDateTime time);
    List<Prediction> findTop10ByTimeGreaterThanOrderByTimeAsc(LocalDateTime time);




}
