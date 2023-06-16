package com.example.pctcback.model;

import jakarta.persistence.*;
import lombok.*;

@Data
@Entity
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Table(name = "Yardstatus")
public class YardStatus {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;
    private String conNumber;
    private String shipCode;
    private Integer Conyear;
    private String voyage;
    private String operatorCode;
    private char fullOrEmpty; // 'F' for full, 'M' for empty
    private String containerSizeCode;
    private String containerTypeCode;
    private Double weightInTons;
    private String destinationCode;
    private String block;
    private Integer bay_x;
    private Integer row_y;
    private Integer tier_z;
    private boolean isExport; // true for export, false for import

}
