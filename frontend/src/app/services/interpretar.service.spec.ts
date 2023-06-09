import { TestBed } from '@angular/core/testing';

import { InterpretarService } from './interpretar.service';

describe('InterpretarService', () => {
  let service: InterpretarService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(InterpretarService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
