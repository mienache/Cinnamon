uint64 inst_count = 0;
uint64 func_count = 0;

select inst I where ((I.opcode) == Load) {
   before I {
       inst_count = inst_count + 1;
   }
}

select func F where (F.isMain) {
   entry F {
      create_checker_thread();
   }
}
exit{
   print_u64(inst_count);
}
