package com.example.pctcback.persistence;

import com.example.pctcback.model.PlannedBlock;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PlannedBlockRepository extends JpaRepository<PlannedBlock, String> {

}
