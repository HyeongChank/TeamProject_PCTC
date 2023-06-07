package com.example.pctcback.persistence;

import com.example.pctcback.model.YardCraneOperation;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;


@Repository
public interface YardOperationRepository extends JpaRepository<YardCraneOperation, Long > {

}
