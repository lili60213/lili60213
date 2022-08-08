Attribute VB_Name = "Module2"
Sub Copy_file()
    Dim gs As Worksheet
    Dim sheet_name, file_name, path_name As String
    
    Dim i As Integer
    For i = 1 To Sheets.count
        sheet_name = Sheets(i).Name
        'current open file path
        path_name = ThisWorkbook.Path
        file_name = Dir(path_name & "\Raw Data\*.csv")
        
        If Len(file_name) Then
            
            Do
                If file_name = sheet_name & ".csv" Then
                    'right to left 7 bit
                    If Right(file_name, 7) = "_GS.csv" Then
                        Debug.Print file_name
                        
                        Workbooks.Open (path_name & "\Raw Data\" & file_name)
                        'open will copy file
                        Windows(file_name).Activate
                        
                        Sheets(sheet_name).Select
                        '1s = 10pieces, 1min = 60*10, 1hr = 60*60*10, 1day = 60*60*24*10=864000
                        Sheets(sheet_name).Range("A2:J864000").Select
                            
                        Selection.Copy
                        
                        ThisWorkbook.Activate
                    
                        Sheets(sheet_name).Select
                        Sheets(sheet_name).Range("A2:J864000").Select
                                
                        ActiveSheet.Paste
                    Else
                        Workbooks.Open (path_name & "\Raw Data\" & file_name)
                        Windows(file_name).Activate
                        Sheets(sheet_name).Select
                        Sheets(sheet_name).Range("A2:F864000").Select
                        
                        Dim RowCount As Integer, GasVolume As Integer
                        RowCount = Range("A3").CurrentRegion.Rows.count
                        GasVolume = 3 'B3
                        For j = 1 To RowCount
                            If Range("B" & GasVolume).Value <> "0" Then 'B3 != 0
                                Rows(GasVolume).Delete Shift:=xlUp 'Delete rows
                            Else
                                GasVolume = GasVolume + 1 'Next row
                                
                            End If
                        Next j
                        Selection.Copy
                                
                        ThisWorkbook.Activate
                        
                        Sheets(sheet_name).Select
                        Sheets(sheet_name).Range("A2:F864000").Select
                                        
                        ActiveSheet.Paste
                                
                    End If
                    
                End If
                Debug.Print file_name
                file_name = Dir
                
            Loop Until Len(file_name) = 0
        End If
    
    Next i

End Sub




