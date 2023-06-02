package com.example.pctcback.persistence;

import com.example.pctcback.model.Ship;
import org.springframework.data.jpa.repository.JpaRepository;


public interface ShipRepository extends JpaRepository <Ship,Long> {

}
