Attribute VB_Name = "Module1"
Sub Cal_freg_count()
    Dim con_freg, count As Integer
    Dim arr() As Integer
    ReDim arr(5)
    
    con_freg = 0
    count = 0
    
    Dim i As Integer
    For i = 3 To Cells(Rows.count, 3).End(xlUp).Row 'Freg : C3 To End
        If Cells(i, "C").Value <= 57 Then
            con_freg = con_freg + 1
        Else
            If con_freg > 0 Then
                If con_freg > UBound(arr) Then 'UBound for Cal Array end index
                    ReDim Preserve arr(con_freg) 'ReDim Preserve for Fix Array index & Preserve for Reserve original value
                End If
                arr(con_freg) = arr(con_freg) + 1 'Count + 1
                con_freg = 0
            End If
        End If
    Next i
    
    For i = 3 To UBound(arr) 'Con_Freg >= 3
        If arr(i) <> 0 Then 'arr(i) != 0
            Cells(i - count, "M").Value = i
            Cells(i - count, "N").Value = arr(i)
        Else
            count = count + 1 'Count = 0 not print
        End If
    Next i
End Sub

